from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import random
from faker import Faker
from uuid import uuid4
from api.models import Customer, Plan, Lead, Opportunities, Sales


fake = Faker("pt_BR")

# -----------------------------
# CONFIGURAÇÕES (fácil escalar)
# -----------------------------

CUSTOMERS_QTD = 90_000
LEADS_QTD = 100_000

PLAN_DISTRIBUTION = {
    "Basic": 60,
    "Premium": 25,
    "Family": 10,
    "Enterprise": 5
}

LEAD_SOURCES = ["Google Ads", "Organic", "LinkedIn", "Referral"]

BUSINESS_GROUPS = ['Varejo', 'Tecnologia', 'Saúde']


# -----------------------------
# Helpers
# -----------------------------

def money(min_cents=5000, max_cents=50000):
    """Gera valores monetários seguros"""
    return Decimal(random.randint(min_cents, max_cents)) / 100


def weighted_plan_choice(plans):
    weights = [PLAN_DISTRIBUTION[p.category] for p in plans]
    return random.choices(plans, weights=weights, k=1)[0]


def create_plans():
    plans_to_create = []

    for category in PLAN_DISTRIBUTION.keys():
        plans_to_create.append(
            Plan(
                plan_id=f"PLN-{category.upper()}",
                name=f"Plano {category}",
                category=category,
                price=money()
            )
        )

    Plan.objects.bulk_create(plans_to_create, ignore_conflicts=True)

    return list(Plan.objects.all())
def generate_customers():
    customers = []

    for _ in range(CUSTOMERS_QTD):

        is_pj = random.random() < 0.35  # 35% empresas

        customers.append(
            Customer(
                customer_cod=str(uuid4()),
                name=fake.company() if is_pj else fake.name(),
                customer_type='pj' if is_pj else 'pf',
                company_name=fake.company() if is_pj else None,
                business_group=random.choice(BUSINESS_GROUPS) if is_pj else None,
                gender=random.choice(['M', 'F', 'Outro']) if not is_pj else None,
                birth_date=fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=70
                ),
                address=fake.address(),
                is_active=random.random() < 0.92
            )
        )

    Customer.objects.bulk_create(customers, batch_size=5000)

    return list(Customer.objects.all())


def generate_sales_flow(customers, plans):

    leads = []
    opportunities = []
    sales = []

    now = timezone.now()

    for _ in range(LEADS_QTD):

        customer = random.choice(customers)
        plan = weighted_plan_choice(plans)

        # Tendência temporal (mais leads recentes)
        lead_date = fake.date_time_between(
            start_date='-18M',
            end_date=now,
            tzinfo=timezone.get_current_timezone()
        )

        lead = Lead(
            customer=customer,
            plan=plan,
            lead_data=lead_date,
            source=random.choice(LEAD_SOURCES)
        )

        leads.append(lead)

    Lead.objects.bulk_create(leads, batch_size=5000)

    leads = list(Lead.objects.select_related('customer', 'plan'))

    for lead in leads:

        # 65% viram oportunidade
        if random.random() > 0.65:
            continue

        open_date = lead.lead_data + timezone.timedelta(
            days=random.randint(1, 10)
        )

        # Premium fecha mais rápido 🙂
        close_days = (
            random.randint(3, 10)
            if lead.plan.category == "Premium"
            else random.randint(7, 25)
        )

        close_date = open_date + timezone.timedelta(days=close_days)

        status = random.choices(
            ['Won', 'Lost', 'Open'],
            weights=[45, 35, 20]
        )[0]

        opp = Opportunities(
            customer=lead.customer,
            plan=lead.plan,
            lead=lead,
            open_date=open_date,
            close_date=close_date,
            status=status,
            source=lead.source
        )

        opportunities.append(opp)

    Opportunities.objects.bulk_create(opportunities, batch_size=5000)

    won_opps = Opportunities.objects.filter(status='Won').select_related(
        'customer', 'plan'
    )

    for opp in won_opps:

        sale_date = opp.close_date + timezone.timedelta(hours=2)

        dependents = (
            random.randint(2, 5)
            if opp.plan.category == "Family"
            else random.randint(0, 2)
        )

        sales.append(
            Sales(
                customer=opp.customer,
                plan=opp.plan,
                opportunities=opp,
                sale_date=sale_date,
                start_plan_data=sale_date,
                end_plan_data = sale_date + timezone.timedelta(days=random.randint(30, 365)),
                monthly_amount=opp.plan.price,
                total_dependents=dependents,
                observation=fake.sentence()
            )
        )

    Sales.objects.bulk_create(sales, batch_size=5000)


# -----------------------------
# Command
# -----------------------------

class Command(BaseCommand):
    help = "Seed profissional para geração massiva de dados"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING("🚀 Iniciando seed PROFISSIONAL..."))

        plans = create_plans()
        customers = generate_customers()
        generate_sales_flow(customers, plans)

        self.stdout.write(self.style.SUCCESS("🔥 Seed finalizado com sucesso!"))
