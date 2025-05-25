import sys
from storage import Storage
from request import Request_Handler


def main(lines):

    storages = {
    "storage_A1": Storage(myu_store=0.01, myu_update=0.0005),
    "storage_A2": Storage(myu_store=0.001, myu_update=0.01)
    }


    for request in lines:
        req = Request_Handler.from_line(request)
        # print(req.req_type, end="  ")
        req.execute(storages)
        





if __name__ == '__main__':

    n = int(input())

    lines = []

    for i in range(n):
        lines.append(input())
        
    """
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    """

    main(lines)

    """
    2022-04-03T12:30 UPLOAD storage_A1 filex 2000000
    2022-04-05T12:30 DELETE storage_B2 targetfile
    2022-04-06T12:30 UPLOAD storage_A2 filey 5
    2022-04-06T12:31 UPLOAD storage_A1 filez 2000000000
    2022-04-10T12:30 DELETE storage_A1 filex
    2022-04-15T12:30 DELETE storage_A2 filey
    2022-05-01T00:00 CALC   
    2022-06-01T00:00 CALC
    """