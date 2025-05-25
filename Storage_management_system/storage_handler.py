import math


class Storage_Handler:
    def __init__(self, storages, storage_name): #dict storages 
        self.storages = storages
        self.storage_name = storage_name
        self.now_storage = storages[storage_name]


    def upload(self, file_name, file_size):
        storage = self.now_storage
        if file_name in storage.files:
            return "UPLOAD: file already exists"
        else: 
            #calc fee if upload and then do upload
            try_status_list = []
            dummy_status = storage.get_status()
            dummy_status["used"] += file_size
            if dummy_status["used"]  > dummy_status["used_max"]:
                dummy_status["used_max"]  = dummy_status["used"] #update max 
            dummy_status["update_size"] += file_size

            try_status_list.append(dummy_status)

            for st in self.storages: #key of storages ⇒ storagenames
                if st != self.storage_name: #dummyに置き換えたstorage(現在のストレージ)以外は普通に計算
                    try_status_list.append(self.storages[st].get_status())
            
            try_fee = calc_fee(try_status_list)

            if (try_fee["storage_fee"] + try_fee["update_fee"]) <= 1000:
                # do upload
                storage.files[file_name] = file_size #upload
                storage.update_status(dummy_status) 

                status_list = [s.get_status() for s in self.storages.values()] #get status by all storages 
                fee = calc_fee(status_list)
                return f"UPLOAD: {fee['storage_fee']} {fee['update_fee']} {fee['usage_fee']}"
            else:
                return "UPLOAD: free plan fee limit exceeded"
    
    def delete(self, file_name):
        storage = self.now_storage
        if file_name not in storage.files:
            return "DELETE: file does not exist"
        else: #calc fee if upload and then do upload
            delete_file_size = storage.files[file_name]
            try_status_list = []
            dummy_status = storage.get_status()
            dummy_status["used"] -= delete_file_size
            dummy_status["update_size"] += delete_file_size 

            try_status_list.append(dummy_status)
            for st in self.storages: #key of storages ⇒ storagenames
                if st != self.storage_name: #dummyに置き換えたstorage(現在のストレージ)以外は普通に計算
                    try_status_list.append(self.storages[st].get_status())
            try_fee = calc_fee(try_status_list)

            if (try_fee["storage_fee"] + try_fee["update_fee"]) <= 1000:
                # do delete
                storage.files.pop(file_name)  #delete
                storage.update_status(dummy_status) 
                status_list = [s.get_status() for s in self.storages.values()] #get status by all storages 
                fee = calc_fee(status_list)
                return f"DELETE: {fee['storage_fee']} {fee['update_fee']} {fee['usage_fee']}"
            else:
                return "DELETE: free plan fee limit exceeded"

    def update(self, file_name, file_size):
        storage = self.now_storage
        if file_name not in storage.files:
            return "UPDATE: file does not exist"
        else:
            #calc fee if upload and then do upload
            updated_file_size = storage.files[file_name]
            try_status_list = []
            dummy_status = storage.get_status()
            dummy_status["used"] = dummy_status["used"] - updated_file_size + file_size
            if dummy_status["used"]  > dummy_status["used_max"]:
                dummy_status["used_max"]  = dummy_status["used"] #update max 
            dummy_status["update_size"] = dummy_status["update_size"] + updated_file_size + file_size

            try_status_list.append(dummy_status)

            for st in self.storages: #key of storages ⇒ storagenames
                if st != self.storage_name: #dummyに置き換えたstorage(現在のストレージ)以外は普通に計算
                    try_status_list.append(self.storages[st].get_status())
            
            try_fee = calc_fee(try_status_list)

            if (try_fee["storage_fee"] + try_fee["update_fee"]) <= 1000:
                # do update
                storage.files[file_name] = file_size #update
                storage.update_status(dummy_status) 

                status_list = [s.get_status() for s in self.storages.values()] #get status by all storages 
                fee = calc_fee(status_list)
                return f"UPDATE: {fee['storage_fee']} {fee['update_fee']} {fee['usage_fee']}"
            else:
                return "UPDATE: free plan fee limit exceeded"



def calc_fee(status_list):
    storage_fee = 0
    update_fee = 0

    for status in status_list:
        # kB ⇒ MB
        used_max = math.ceil(status["used_max"] / 1000)
        update_size = math.ceil(status["update_size"] / 1000)
        # calc sum fee
        storage_fee += math.ceil(used_max * status["myu_store"])
        update_fee  += math.ceil(update_size * status["myu_update"])

    usage_fee = max(0, storage_fee + update_fee - 1000)

    return {
        "storage_fee": storage_fee,
        "update_fee": update_fee,
        "usage_fee": usage_fee
    }
