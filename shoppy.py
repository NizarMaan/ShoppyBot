"""ShoppyBot written by Nizar Maan Chehaeb"""
from Models.payment import *
from settings import Settings

def main():
    """ShoppyBot entry point"""
    settings = Settings()

    checkout_profiles = []

    payment_option_0 = PaymentOption(
        CreditCard("5466042028174546", "3/23", "332"),
        Address("Christopher", "Cunanan", "110 Beechwood Avenue",
                "Mount Vernon", "NY", "US", "10553", "914-314-6010", "kevinudasco@exqtrading.com")
        )

    checkout_profile_0 = CheckoutProfile(
        payment_option_0.credit_card,
        payment_option_0.billing_address,
        payment_option_0.billing_address,
        payment_option_0
        )

    checkout_profiles.append(checkout_profile_0)

if __name__ == '__main__':
    main()
