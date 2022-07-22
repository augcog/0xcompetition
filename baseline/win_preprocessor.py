
class Preprocessor:
    """
    This is the base Preprocessor class that will be using for
    any data preprocessing required
    """

    def __init__(self, df):
        self.df = df

    def clean(self):
        self.remove_features()
        self.drop_duplicates()
        self.drop_nones()

    def remove_features(self, inference=False):
        """
        This method removes unnecessary features

        Returns:

        df = a DataFrame without unneeded features
        """
        # Remove unnecessary fields
        self.df.drop(['max_fee_per_gas', 'max_priority_fee_per_gas', 'receipt_cumulative_gas_used',
                      'receipt_gas_used', 'receipt_contract_address', 'receipt_root', 'receipt_status',
                      'receipt_effective_gas_price'], axis=1, inplace=True)

    def drop_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_nones(self):
        self.df.dropna(inplace=True)