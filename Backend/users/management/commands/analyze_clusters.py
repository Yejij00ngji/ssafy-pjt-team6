from django.core.management.base import BaseCommand
import pandas as pd
from users.models import FinancialProfile

class Command(BaseCommand):
    help = "클러스터별 금융 성향 해석 리포트 출력"

    def handle(self, *args, **options):
        qs = FinancialProfile.objects.all().values(
            'cluster_label',
            'annual_income_amt',
            'invest_eval_amt',
            'balance_amt',
            'withdrawable_amt',
            'expense_growth_rate',
            'expense_to_income_ratio'
        )

        df = pd.DataFrame(list(qs))
        df['total_assets'] = df['invest_eval_amt'] + df['balance_amt']
        df['inv_ratio'] = df['invest_eval_amt'] / (df['total_assets'] + 1)
        df['withdrawable_ratio'] = df['withdrawable_amt'] / (df['total_assets'] + 1)

        summary = df.groupby('cluster_label').agg({
            'annual_income_amt': 'mean',
            'inv_ratio': 'mean',
            'withdrawable_ratio': 'mean',
            'expense_growth_rate': 'mean',
            'expense_to_income_ratio': 'mean',
            'cluster_label': 'count'
        }).rename(columns={'cluster_label': 'user_count'})

        self.stdout.write(self.style.SUCCESS("\n[Cluster Interpretation Report]"))
        self.stdout.write(summary.round(3).to_string())
