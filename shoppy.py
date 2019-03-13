"""ShoppyBot written by Nizar Maan Chehaeb"""
from Models.payment import *
from Models.items import Shoes
from Bots.exclucitybot import ExclucityBot
from Bots.yeezybot import YeezyBot


def main():
    """ShoppyBot entry point"""
    checkout_profiles = []

    payment_option_0 = PaymentOption(
        Address("Christopher", "Cunanan", "110 Beechwood Avenue",
                "Mount Vernon", "AB", "CA", "T3H 0L4", "9143146010", "kevinudasco@exqtrading.com"),
        CreditCard("5466 0420 2817 4543", "03/99", "999")
    )

    checkout_profile_0 = CheckoutProfile(
        payment_option_0.credit_card,
        payment_option_0.billing_address,
        payment_option_0.billing_address,
        payment_option_0
    )

    checkout_profiles.append(checkout_profile_0)

    #exclucity_bot = ExclucityBot(checkout_profiles)
    # shoe_exlucity = Shoes(item_name="Air Jordan 4 Retro 'Flight Nostalgia'",
    # purchase_quantity=1, size=11)
    # exclucity_bot.purchase_item(shoe_exlucity)

    shoe_yeezy = Shoes(item_name="Air Jordan 4 Retro 'Flight Nostalgia'",
                       purchase_quantity=1, size=11)
    yeezy_bot = YeezyBot(checkout_profiles)
    yeezy_bot.purchase_item(shoe_yeezy)


if __name__ == '__main__':
    main()
