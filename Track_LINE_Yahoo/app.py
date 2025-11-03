from typing import List, Dict, Tuple
from domain import NetCafe, TypePricing
from util import parse_time

def run(lines: List[str]) -> str:
    it = iter(lines)

    # 基本情報
    n, m, cleaning_duration_seat = map(int, next(it).split())
    seat_types = list(map(int, next(it).split()))
    assert len(seat_types) == n

    # 料金情報
    pricing_by_type: Dict[int, TypePricing] = {}
    for type_id in range(1, m + 1):
        basic_s, p_s = next(it).split()
        basic, p = int(basic_s), int(p_s)
        packs: List[Tuple[int, int]] = []
        for _ in range(p):
            pt, pp = map(int, next(it).split())
            packs.append((pt, pp))
        pricing_by_type[type_id] = TypePricing(basic=basic, packs=packs)

    # フード情報
    f = int(next(it))
    food_price = list(map(int, next(it).split()))
    assert len(food_price) == f

    # クーポン
    c = int(next(it))
    coupon_meta: Dict[int, Tuple[int, int]] = {}
    for cid in range(1, c + 1):
        tgt, disc = map(int, next(it).split())
        coupon_meta[cid] = (tgt, disc)

    # シャワー
    s, shower_charge, cleaning_duration_shower = map(int, next(it).split())

    # クエリ
    q = int(next(it))

    cafe = NetCafe(
        n=n,
        m=m,
        seat_types=seat_types,
        pricing_by_type=pricing_by_type,
        food_price=food_price,
        s=s,
        shower_charge=shower_charge,
        cleaning_duration_seat=cleaning_duration_seat,
        cleaning_duration_shower=cleaning_duration_shower,
        coupon_meta=coupon_meta,
    )

    out_lines: List[str] = []
    for _ in range(q):
        line = next(it)
        if line.startswith("checkin: "):
            _, ts, seat_type_s = line.split()
            now = parse_time(ts)
            seat_type = int(seat_type_s)
            out_lines.append(cafe.q_checkin(now, seat_type))
        elif line.startswith("get-duration: "):
            _, ts, seat_id_s = line.split()
            now = parse_time(ts)
            seat_id = int(seat_id_s)
            out_lines.append(cafe.q_get_duration(now, seat_id))
        elif line.startswith("checkout: "):
            parts = line.split()
            ts = parts[1]
            now = parse_time(ts)
            uid = int(parts[2])
            k = int(parts[3]) if len(parts) >= 4 else 0
            coupon_ids = list(map(int, parts[4:4 + k])) if k > 0 else []
            out_lines.append(cafe.q_checkout(now, uid, coupon_ids))
        elif line.startswith("order-food: "):
            _, ts, seat_id_s, food_id_s = line.split()
            now = parse_time(ts)
            seat_id = int(seat_id_s)
            food_id = int(food_id_s)
            out_lines.append(cafe.q_order_food(now, seat_id, food_id))
        elif line.startswith("shower-start: "):
            _, ts, seat_id_s = line.split()
            now = parse_time(ts)
            seat_id = int(seat_id_s)
            out_lines.append(cafe.q_shower_start(now, seat_id))
        elif line.startswith("shower-end: "):
            _, ts, seat_id_s = line.split()
            now = parse_time(ts)
            seat_id = int(seat_id_s)
            out_lines.append(cafe.q_shower_end(now, seat_id))
        elif line.startswith("get-vacant-seats: "):
            _, ts = line.split()
            now = parse_time(ts)
            out_lines.append(cafe.q_get_vacant_seats(now))
        else:
            pass
    return "\n".join(out_lines) + ("\n" if out_lines else "")
