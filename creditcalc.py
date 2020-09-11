import math
import argparse
import sys


def annuity_payment(principal, months, interest):
    """Counts and prints annuity payment"""
    result = math.ceil(principal * ((interest * (1 + interest) ** months) /
                                    ((1 + interest) ** months - 1)))
    print(f"Your annuity payment = {result}!")
    print(f'Overpayment = {round(result * months - principal)}')


def count_interest(interest):
    """Counts nominal interest rate"""
    return interest / (12 * 100)


def credit_principal(annuity, interest, months):
    """Count credit principal on given annuity interest and months"""
    result = annuity / ((interest * (1 + interest) ** months) /
                        ((1 + interest) ** months - 1))
    print(f"Your credit principal = {int(result)}!")
    print(f'Overpayment = {int(annuity * months - int(result))}')


def mth_diff_payment(principal, interest, months, c_month):
    """Calculates differentiated payments"""
    return math.ceil((principal / months) + interest * (principal - ((principal * (c_month - 1)) / months)))


def calc_diff_months(principal, interest, periods):
    """Prints each month differentiated payment and overpayment"""
    overpayment = 0
    for i in range(1, periods + 1):
        result = mth_diff_payment(principal, interest, periods, i)
        overpayment += result
        print(f'Month {i}: payment is {result}')
    print(f'\nOverpayment = {round(overpayment - principal)}')


def print_years_months(years, months):
    """Prints how many months and years credit will be payed"""
    result = "It will take "
    if years:
        result += str(years)
        result += " years " if years > 1 else " year "
    if years and months:
        result += "and "
    if months:
        result += str(months)
        result += " months " if months > 1 else " month "
    result += "to repay this loan!"
    print(result)


def count_monthly_payments(principal, payment, interest):
    """Counts number of months to pay certain credit with annual rate with logarithmic formula and prints result"""
    months = math.ceil(math.log(payment / (payment - interest * principal),
                                (interest + 1)))
    years = months // 12
    print_years_months(years, months % 12)
    print(f'Overpayment = {int(payment * months - principal)}')


def calc_credit(args):
    if args.type == "diff":
        calc_diff_months(args.principal, count_interest(args.interest), args.periods)
    else:
        if args.periods is None:
            count_monthly_payments(args.principal, args.payment, count_interest(args.interest))
        if args.payment is None:
            annuity_payment(args.principal, args.periods, count_interest(args.interest))
        if args.principal is None:
            credit_principal(args.payment, count_interest(args.interest), args.periods)


def validity_check(args) -> bool:
    """Checking arguments for errors and conflicts"""
    all_args = [args.payment, args.principal, args.periods, args.interest]
    if not 3 < len(sys.argv[1:]) < 6 or args.interest is None or args.type not in ("diff", "annuity"):
        return False
    for n in all_args:
        if n is not None and n < 0:
            return False
    # Conflict diff with payment
    if args.payment is not None and args.type == "diff":
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    args = parser.parse_args()
    if validity_check(args):
        calc_credit(args)
    else:
        print("Incorrect parameters")


if __name__ == "__main__":
    main()








