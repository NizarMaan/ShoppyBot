"""ShoppyBot written by Nizar Maan Chehaeb"""
from Models.payment import *
from Models.items import Shoes
from Bots.exclucitybot import ExclucityBot


def main():
    """ShoppyBot entry point"""
    checkout_profiles = []

    payment_option_0 = PaymentOption(
        Address("Christopher", "Cunanan", "110 Beechwood Avenue",
                "Mount Vernon", "AB", "CA", "T3H 0L4", "9143146010", "kevinudasco@exqtrading.com"),
        CreditCard("5466042028174543", "3/23", "332")
    )

    checkout_profile_0 = CheckoutProfile(
        payment_option_0.credit_card,
        payment_option_0.billing_address,
        payment_option_0.billing_address,
        payment_option_0
    )

    checkout_profiles.append(checkout_profile_0)

    exclucity_bot = ExclucityBot(checkout_profiles)
    shoe = Shoes(item_name="Air Jordan 4 Retro 'Flight Nostalgia'",
                 purchase_quantity=1, size=11)
    exclucity_bot.purchase_item(shoe)


if __name__ == '__main__':
    main()
