from storage_handler import Storage_Handler
from storage_handler import calc_fee


#Request class
class Request:
    def __init__(self, time, req_type, storagename, filename):
        self.time = time
        self.req_type = req_type
        self.storage_name = storagename
        self.file_name = filename
    
    # True for storage_name starts with "storage_A.....""
    def is_valid_storage(self):
        return self.storage_name.startswith("storage_A")




class Upload(Request):
    def __init__(self, time, req_type, storagename, filename, filesize):
        super().__init__(time, req_type, storagename, filename)
        self.file_size = int(filesize)

    def execute(self, storages):
        if not self.is_valid_storage():
            print(f"{self.req_type}: this storage location is not available on the free plan")
        else:
            #do
            # print("execute")
            handler = Storage_Handler(storages, self.storage_name)
            print(handler.upload(self.file_name, self.file_size))
            


class Delete(Request):
    def __init__(self, time, req_type, storagename, filename):
        super().__init__(time, req_type, storagename, filename)

    def execute(self, storages):
        if not self.is_valid_storage():
            print(f"{self.req_type}: this storage location is not available on the free plan")
        else:
            #do
            # print("execute")
            handler = Storage_Handler(storages, self.storage_name)
            print(handler.delete(self.file_name))


class Update(Request):
    def __init__(self, time, req_type, storagename, filename, filesize):
        super().__init__(time, req_type, storagename, filename)
        self.file_size = int(filesize)

    def execute(self, storages):
        if not self.is_valid_storage():
            print(f"{self.req_type}: this storage location is not available on the free plan")
        else:
            #do
            # print("execute")
            handler = Storage_Handler(storages, self.storage_name)
            print(handler.update(self.file_name, self.file_size))

class Calc:
    def __init__(self, time, req_type):
        self.time = time
        self.req_type = req_type

    def execute(self, storages):
        #do
        # print("execute")
        status_list = [s.get_status() for s in storages.values()] #get status by all storages 
        fee = calc_fee(status_list)
        print(f"CALC: [{int(storages["storage_A1"].used)} {int(storages["storage_A2"].used)} 0 0] {fee["storage_fee"]} {fee["update_fee"]} {fee["usage_fee"]}")

        for s in storages.values():
            s.used_max = s.used
            s.update_size = 0


#Judge Which Request 
class Request_Handler:
    @staticmethod
    def from_line(line):
        parts = line.strip().split()
        req_type = parts[1]

        if req_type == "UPLOAD":
            return Upload(parts[0], parts[1], parts[2], parts[3], parts[4])
        elif req_type == "DELETE":
            return Delete(parts[0], parts[1], parts[2], parts[3])
        elif req_type == "UPDATE":
            return Update(parts[0], parts[1], parts[2], parts[3], parts[4])
        elif req_type == "CALC":
            return Calc(parts[0], parts[1])
        else:
            raise ValueError(f"Unknown request type")

