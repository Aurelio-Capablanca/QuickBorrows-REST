from datetime import datetime


def calculate_payment_plan(total: float, initial_times: list, aim_to_pay: list, generate_to_fill: bool):
    payment_plan = []
    ## Single Element Lists
    if not generate_to_fill and len(initial_times) == 1 and len(aim_to_pay) == 1:  # pay by full set of times
        bill_times = initial_times[0]
        bill_pay = round(total / bill_times, 2)
        payment_plan.append({"bill_pay ": bill_pay, "bill_times": bill_times})
        print(payment_plan)
        return payment_plan
    if generate_to_fill == True and aim_to_pay is not None:  # pay by stated initial Bill
        bill_set = int(total / aim_to_pay[0])
        initial_amount = bill_set * aim_to_pay[0]
        final_payment = total - initial_amount
        print("aim to pay : ", aim_to_pay[0], " Initial Payment: ", initial_amount)
        payment_plan.append({"bill_pay ": aim_to_pay[0], "bill_times": bill_set})
        payment_plan.append({"bill_pay ": final_payment, "bill_times": 1})
        print(payment_plan)
        return payment_plan
    ## Single Element Lists
    ## Multiple Elements List
    if len(initial_times) > 0 and len(aim_to_pay) > 0:  ## Pay by appoint but with rightful intervention
        accumulated_payment = [0]
        set_to_fix = []
        for index, value in enumerate(aim_to_pay):
            print(index)
            accumulated_payment[0] += aim_to_pay[index] * initial_times[index]
            if accumulated_payment[0] < total:
                print("rightful! ", accumulated_payment[0], " ",
                      {"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
                payment_plan.append({"bill_pay ": aim_to_pay[index], "bill_times": initial_times[index]})
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
            print(payment_plan)
        return None
    ## Multiple Elements List
    return payment_plan


if __name__ == "__main__":
    calculate_payment_plan(1650, [10, 3], [100, 216.67], False)
