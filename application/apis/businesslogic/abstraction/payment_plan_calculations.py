from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta

from application.apis.models.issued_bill_model import IssuedBill


def calculate_issued_bill(total: float, initial_times: list[int], aim_to_pay: list[float], generate_to_fill: bool,
                          id_origin: int,
                          initial_date: datetime):
    bill_issues = []

    ## CASE 1:  pay by full set of times
    if not generate_to_fill and len(initial_times) == 1 and len(aim_to_pay) == 0:
        bill_times = initial_times[0]
        bill_pay = round(total / bill_times, 2)
        for index in range(bill_times):
            bill_issues.append(IssuedBill(amounttopay=bill_pay, duedate=initial_date + relativedelta(months=index),
                                          idborrow=id_origin))
        return bill_issues

    ## CASE 2:  pay by stated initial Bill
    if generate_to_fill == True and aim_to_pay is not None:
        agreed_amount = aim_to_pay[0]
        bill_set = int(total / agreed_amount)
        for i in range(bill_set):
            bill_issues.append(IssuedBill(amounttopay=agreed_amount, duedate=initial_date + relativedelta(months=i),
                                          idborrow=id_origin))
        final_payment = round(total - (agreed_amount * bill_set), 2)
        if final_payment > 0:
            bill_issues.append(
                IssuedBill(amounttopay=final_payment, duedate=initial_date + relativedelta(months=bill_set),
                           idborrow=id_origin))
        return bill_issues

    ##CASE 3 : Pay by appoint but with rightful intervention
    if len(initial_times) == len(aim_to_pay):
        current_month = 0
        total_paid = 0.0
        for i in range(len(initial_times)):
            pay_count = initial_times[i]
            pay_amount = aim_to_pay[i]
            for j in range(pay_count):
                due = initial_date + relativedelta(months=current_month)
                current_month += 1
                if round(total_paid + pay_amount, 2) >= total:
                    pay_amount = round(total - total_paid, 2)
                    if pay_amount <= 0:
                        break
                    bill_issues.append(IssuedBill(amounttopay=pay_amount, duedate=due, idborrow=id_origin))
                    return bill_issues
                bill_issues.append(IssuedBill(amounttopay=pay_amount, duedate=due, idborrow=id_origin))
                total_paid += pay_amount
        return bill_issues
    return bill_issues


if __name__ == "__main__":
    first_case = calculate_issued_bill(1650, [5], [], False, 0, datetime.now(timezone.utc))
    second_case = calculate_issued_bill(1968, [10], [100], True, 0, datetime.now(timezone.utc))
    third_case = calculate_issued_bill(1968, [10, 3], [100, 516.67], False, 0, datetime.now(timezone.utc))
    print("****************************************************************")
    for a, val in enumerate(first_case):
        print(first_case[a])
    print("****************************************************************")
    for a, val in enumerate(second_case):
        print(second_case[a])
    print("****************************************************************")
    for a, val in enumerate(third_case):
        print((a + 1), " - ", third_case[a])
    print("****************************************************************")
