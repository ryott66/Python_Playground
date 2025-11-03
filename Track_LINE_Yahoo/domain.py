from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from util import seconds_between, minutes_ceil_from_seconds, seat_tick_count, shower_tick_count

# 料金モデル
@dataclass(frozen=True)
class TypePricing:
    basic: int
    packs: List[Tuple[int, int]]

# 利用者
@dataclass
class User:
    uid: int
    seat_id: int
    seat_type: int
    checkin_at: datetime
    done: bool = False
    # 課金
    food_fee: int = 0
    shower_fee: int = 0
    # クーポン：フード注文回数
    food_counts: Dict[int, int] = field(default_factory=dict)
    # シャワー使用
    shower_id_in_use: Optional[int] = None
    shower_started_at: Optional[datetime] = None

class NetCafe:
    def __init__(
        self,
        n: int,
        m: int,
        seat_types: List[int],
        pricing_by_type: Dict[int, TypePricing],
        food_price: List[int],
        s: int,
        shower_charge: int,
        cleaning_duration_seat: int = 0,
        cleaning_duration_shower: int = 0,
        coupon_meta: Optional[Dict[int, Tuple[int, int]]] = None,
    ):
        self.n = n
        self.m = m
        self.seat_types = seat_types
        self.pricing_by_type = pricing_by_type
        self.food_price = food_price
        self.s = s
        self.shower_charge = shower_charge
        self.cleaning_duration_seat = cleaning_duration_seat
        self.cleaning_duration_shower = cleaning_duration_shower
        self.coupon_meta = coupon_meta or {}

        # タイプごとの空席ヒープ
        self.free_seats_by_type: Dict[int, List[int]] = {t: [] for t in range(1, m + 1)}
        for seat_id in range(1, n + 1):
            t = seat_types[seat_id - 1]
            heapq.heappush(self.free_seats_by_type[t], seat_id)

        # 現在のシート占有状況: seat_id -> uid or None
        self.seat_user: List[Optional[int]] = [None] * (n + 1)

        # 清掃中シート
        self.cleaning_seats: List[Tuple[int, int, int]] = []

        # ユーザー
        self.users: Dict[int, User] = {}
        self.next_user_id: int = 1

        # シャワー空き
        self.free_showers: List[int] = list(range(1, s + 1))
        heapq.heapify(self.free_showers)

        # 清掃中シャワー
        self.cleaning_showers: List[Tuple[int, int]] = []

    @staticmethod
    def _to_ts(dt: datetime) -> int:
        return int(dt.timestamp())

    def _flush_cleaning_until(self, now: datetime) -> None:
        now_ts = self._to_ts(now)
        # シャワーの解放
        while self.cleaning_showers and self.cleaning_showers[0][0] <= now_ts:
            _, shower_id = heapq.heappop(self.cleaning_showers)
            heapq.heappush(self.free_showers, shower_id)

        # 座席の解放
        while self.cleaning_seats and self.cleaning_seats[0][0] <= now_ts:
            _, seat_id, seat_type = heapq.heappop(self.cleaning_seats)
            heapq.heappush(self.free_seats_by_type[seat_type], seat_id)

    def calc_seat_fee(self, seat_type: int, dur_sec: int) -> int:
        pr = self.pricing_by_type[seat_type]
        best = seat_tick_count(dur_sec) * pr.basic
        for pack_time_min, pack_price in pr.packs:
            over_sec = max(0, dur_sec - pack_time_min * 60)
            cost = pack_price + seat_tick_count(over_sec) * pr.basic
            if cost < best:
                best = cost
        return best

    def q_checkin(self, now: datetime, seat_type: int) -> str:
        self._flush_cleaning_until(now)
        heap = self.free_seats_by_type[seat_type]
        if not heap:
            return "checkin: fully occupied"
        seat_id = heapq.heappop(heap)
        uid = self.next_user_id
        self.next_user_id += 1

        user = User(
            uid=uid,
            seat_id=seat_id,
            seat_type=seat_type,
            checkin_at=now,
            done=False,
            food_fee=0,
            shower_fee=0,
            food_counts={},
        )
        self.users[uid] = user
        self.seat_user[seat_id] = uid
        return f"checkin: userid = {uid}, seatid = {seat_id}"

    def _seat_used_or_err(self, seat_id: int) -> Optional[str]:
        uid = self.seat_user[seat_id]
        if uid is None:
            return "seat not used"
        return None

    def q_get_duration(self, now: datetime, seat_id: int) -> str:
        self._flush_cleaning_until(now)
        err = self._seat_used_or_err(seat_id)
        if err:
            return f"get-duration: {err}"
        uid = self.seat_user[seat_id]
        user = self.users[uid]
        dur_sec = seconds_between(now, user.checkin_at)
        mins = minutes_ceil_from_seconds(dur_sec)
        return f"get-duration: {mins}"

    def q_order_food(self, now: datetime, seat_id: int, food_id: int) -> str:
        self._flush_cleaning_until(now)
        err = self._seat_used_or_err(seat_id)
        if err:
            return f"order-food: {err}"
        uid = self.seat_user[seat_id]
        user = self.users[uid]
        price = self.food_price[food_id - 1]
        user.food_fee += price
        user.food_counts[food_id] = user.food_counts.get(food_id, 0) + 1
        return "order-food: ok"

    def q_shower_start(self, now: datetime, seat_id: int) -> str:
        self._flush_cleaning_until(now)
        err = self._seat_used_or_err(seat_id)
        if err:
            return f"shower-start: {err}"
        uid = self.seat_user[seat_id]
        user = self.users[uid]
        if user.shower_id_in_use is not None:
            return "shower-start: already started"
        if not self.free_showers:
            return "shower-start: fully occupied"
        shower_id = heapq.heappop(self.free_showers)
        user.shower_id_in_use = shower_id
        user.shower_started_at = now
        return f"shower-start: {shower_id}"

    def q_shower_end(self, now: datetime, seat_id: int) -> str:
        self._flush_cleaning_until(now)
        err = self._seat_used_or_err(seat_id)
        if err:
            return f"shower-end: {err}"
        uid = self.seat_user[seat_id]
        user = self.users[uid]
        if user.shower_id_in_use is None or user.shower_started_at is None:
            return "shower-end: not started"

        dur_sec = seconds_between(now, user.shower_started_at)
        mins = minutes_ceil_from_seconds(dur_sec)
        user.shower_fee += shower_tick_count(dur_sec) * self.shower_charge

        shower_id = user.shower_id_in_use
        user.shower_id_in_use = None
        user.shower_started_at = None

        if self.cleaning_duration_shower <= 0:
            heapq.heappush(self.free_showers, shower_id)
        else:
            available_at_ts = self._to_ts(now) + self.cleaning_duration_shower * 60
            heapq.heappush(self.cleaning_showers, (available_at_ts, shower_id))
        return f"shower-end: {mins}"

    def q_checkout(self, now: datetime, uid: int, coupon_ids: List[int]) -> str:
        self._flush_cleaning_until(now)
        user = self.users.get(uid)
        if user is None:
            return "checkout: invalid user"
        if user.done:
            return "checkout: already done"
        if user.shower_id_in_use is not None:
            return "checkout: shower is still in use"

        # クーポン検証
        discount_total = 0
        if coupon_ids:
            max_discount_by_food: Dict[int, int] = {}
            for cid in coupon_ids:
                tgt, disc = self.coupon_meta[cid]
                max_discount_by_food[tgt] = max(max_discount_by_food.get(tgt, 0), disc)

            for food_id, max_disc in max_discount_by_food.items():
                if user.food_counts.get(food_id, 0) <= 0:
                    return "checkout: invalid coupon"

            for food_id, max_disc in max_discount_by_food.items():
                cnt = user.food_counts.get(food_id, 0)
                if cnt > 0:
                    discount_total += max_disc * cnt

        # 料金計算
        dur_sec = seconds_between(now, user.checkin_at)
        seat_fee = self.calc_seat_fee(user.seat_type, dur_sec)
        food_fee_after = max(0, user.food_fee - discount_total)
        total = seat_fee + food_fee_after + user.shower_fee

        # 精算済 & 座席を解放（清掃対応）
        user.done = True
        seat_id = user.seat_id
        self.seat_user[seat_id] = None

        if self.cleaning_duration_seat <= 0:
            heapq.heappush(self.free_seats_by_type[user.seat_type], seat_id)
        else:
            available_at_ts = self._to_ts(now) + self.cleaning_duration_seat * 60
            heapq.heappush(self.cleaning_seats, (available_at_ts, seat_id, user.seat_type))
        return f"checkout: {total}"

    def q_get_vacant_seats(self, now: datetime) -> str:
        self._flush_cleaning_until(now)
        items: List[Tuple[int, int]] = []
        for t in range(1, self.m + 1):
            cnt = len(self.free_seats_by_type[t])
            if cnt > 0:
                items.append((t, cnt))

        # 出力仕様
        items.sort(key=lambda x: x[0])
        lines = [f"get-vacant-seats: {len(items)}"]
        for t, cnt in items:
            lines.append(f"{t} {cnt}")
        return "\n".join(lines)
