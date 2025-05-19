from datetime import datetime, timezone

from application.apis.models.issued_bill_model import IssuedBill


def calculate_payment_plan(total: float, initial_times: list, aim_to_pay: list, generate_to_fill: bool, id_plan: int,
                           initial_date: datetime):
    bill_issues = []  ## the idea is to return the set of the whole bills issues,
    # as those are the main goal to save from here, Payment Plan can go by stand alone
    ## Single Element Lists
    if not generate_to_fill and len(initial_times) == 1 and len(aim_to_pay) == 0:  # pay by full set of times
        print("****************************************************************")
        print(" pay by full set of times ")
        bill_times = initial_times[0]
        bill_pay = round(total / bill_times, 2)
        for i in range(bill_times):
            bill_issues.append({"bill_pay ": bill_pay, "bill_times": bill_times})
            ##bill_issues.append(IssuedBill(amounttopay=bill_pay))
        #payment_plan.append({"bill_pay ": bill_pay, "bill_times": bill_times})
        print(bill_issues)
        print("****************************************************************")
        return bill_issues
    if generate_to_fill == True and aim_to_pay is not None:  # pay by stated initial Bill
        print("****************************************************************")
        print(" pay by stated initial Bill ")
        bill_set = int(total / aim_to_pay[0])
        initial_amount = bill_set * aim_to_pay[0]
        for i in range(bill_set):
            bill_issues.append({"bill_pay ": aim_to_pay[0], "bill_times": bill_set})
        final_payment = total - initial_amount
        print("aim to pay : ", aim_to_pay[0], " Initial Payment: ", initial_amount)
        bill_issues.append({"bill_pay ": final_payment, "bill_times": 1})
        print(bill_issues)
        print("****************************************************************")
        return bill_issues
    ## Single Element Lists
    ## Multiple Elements List
    if len(initial_times) > 0 and len(aim_to_pay) > 0:  ## Pay by appoint but with rightful intervention
        print("****************************************************************")
        print(" Pay by appoint but with rightful intervention ")
        accumulated_payment = [0]
        set_to_fix = []
        for index, value in enumerate(aim_to_pay):
            print(index)
            accumulated_payment[0] += aim_to_pay[index] * initial_times[index]
            if accumulated_payment[0] < total:
                print("rightful! ", accumulated_payment[0], " ",
                      {"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
                bill_issues.append({"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
            else:
                print("this shouldn't be! ", accumulated_payment[0], "  ",
                      {"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
                remove_from_payment = round(accumulated_payment[0] - total, 2)
                print("operation : total", total, " -  accumulated : ", accumulated_payment[0], " = ",
                      remove_from_payment)
                for i in range(initial_times[index]):
                    set_to_fix.append(aim_to_pay[index])
                set_to_fix[len(set_to_fix) - 1] = round(set_to_fix[len(set_to_fix) - 1] - remove_from_payment, 2)
                print("Array set to fix values : ", set_to_fix)
            # payment_plan.append({"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
            print(bill_issues)
        print("****************************************************************")
        return bill_issues
    ## Multiple Elements List
    return bill_issues


if __name__ == "__main__":
    calculate_payment_plan(1650, [5], [], False, 0, datetime.now(timezone.utc))
    calculate_payment_plan(1650, [10], [100], True, 0, datetime.now(timezone.utc))
    calculate_payment_plan(1650, [10, 3], [100, 216.67], False,0, datetime.now(timezone.utc))
