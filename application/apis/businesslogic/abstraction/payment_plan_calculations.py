from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from application.apis.models.issued_bill_model import IssuedBill


def calculate_payment_plan(total: float, initial_times: list, aim_to_pay: list, generate_to_fill: bool,
                           id_plan_origin: int,
                           initial_date: datetime):
    bill_issues = []
    if not generate_to_fill and len(initial_times) == 1 and len(aim_to_pay) == 0:  # pay by full set of times
        bill_times = initial_times[0]
        bill_pay = round(total / bill_times, 2)
        for index in range(bill_times):
            bill_issues.append(IssuedBill(amounttopay=bill_pay, duedate=initial_date + relativedelta(months=index),
                                          idplan=id_plan_origin))
        return bill_issues
    if generate_to_fill == True and aim_to_pay is not None:  # pay by stated initial Bill
        bill_set = int(total / aim_to_pay[0])
        initial_amount = bill_set * aim_to_pay[0]
        for i in range(bill_set):
            bill_issues.append(IssuedBill(amounttopay=aim_to_pay[0], duedate=initial_date + relativedelta(months=i),
                                          idplan=id_plan_origin))
        final_payment = total - initial_amount
        bill_issues.append(
            IssuedBill(amounttopay=final_payment, duedate=initial_date + relativedelta(months=bill_set + 1),
                       idplan=id_plan_origin))
        return bill_issues
    ## Single Element Lists
    ## Multiple Elements List
    if len(initial_times) > 0 and len(aim_to_pay) > 0:  ## Pay by appoint but with rightful intervention
        accumulated_payment = [0]
        set_to_fix = []
        for index, value in enumerate(aim_to_pay):
            accumulated_payment[0] += aim_to_pay[index] * initial_times[index]
            if accumulated_payment[0] < total:  ## Everything is Still Correct
                for indexOne in range(initial_times[index]):
                    bill_issues.append(
                        IssuedBill(amounttopay=aim_to_pay[0], duedate=initial_date + relativedelta(months=indexOne),
                                   idplan=id_plan_origin))
            else:
                remove_from_payment = round(accumulated_payment[0] - total, 2)
                ## fix if the remnant is too big to cut the previous payment if needed
                for iTwo in range(initial_times[index]):
                    set_to_fix.append(aim_to_pay[index])
                    bill_issues.append(IssuedBill(amounttopay=set_to_fix[0],
                                                  duedate=initial_date + relativedelta(months=initial_times[index]),
                                                  idplan=id_plan_origin))
                final_fix = round(set_to_fix[len(set_to_fix) - 1] - remove_from_payment, 2)
                bill_issues[len(bill_issues) - 1].amounttopay = final_fix
        return bill_issues
    ## Multiple Elements List
    return bill_issues


if __name__ == "__main__":
    first_case = calculate_payment_plan(1650, [5], [], False, 0, datetime.now(timezone.utc))
    second_case = calculate_payment_plan(1650, [10], [100], True, 0, datetime.now(timezone.utc))
    third_case = calculate_payment_plan(1650, [10, 3], [100, 216.67], False, 0, datetime.now(timezone.utc))
    print("****************************************************************")
    for i, val in enumerate(first_case):
        print(first_case[i])
    print("****************************************************************")
    for i, val in enumerate(second_case):
        print(second_case[i])
    print("****************************************************************")
    for i, val in enumerate(third_case):
        print(third_case[i])
    print("****************************************************************")
