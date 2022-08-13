
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
        self.df.drop(['index', 'address'], axis=1, inplace=True)

    def drop_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_nones(self):
        self.df.dropna(inplace=True)