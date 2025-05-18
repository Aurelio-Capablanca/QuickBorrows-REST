from datetime import datetime


def calculate_payment_plan(total: float, initial_times: list, aim_to_pay: list, generate_to_fill: bool, start_date: datetime, end_date: datetime):
    payment_plan = []
    ## Single Element Lists
    if not generate_to_fill:#pay by full set of times
        #replace with actual model to process
        bill_times = initial_times[0]
        bill_pay = round(total / bill_times, 2)
        payment_plan.append({"bill_pay ": bill_pay, "bill_times": bill_times})
        print(payment_plan)
        return payment_plan
    if generate_to_fill==True and aim_to_pay is not None:#pay by stated initial Bill
        bill_set = int(total / aim_to_pay[0])
        initial_amount = bill_set * aim_to_pay[0]
        final_payment = total - initial_amount
        print("aim to pay : ",aim_to_pay[0]," Initial Payment: ",initial_amount)
        payment_plan.append({"bill_pay ": aim_to_pay[0], "bill_times": bill_set})
        payment_plan.append({"bill_pay ": final_payment, "bill_times": 1})
        print(payment_plan)
        return None
    ## Single Element Lists
    return None

if __name__ == "__main__":
    calculate_payment_plan(1650, [3], [500], True, None, None)