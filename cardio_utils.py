import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class IQRClipper(BaseEstimator, TransformerMixin):
    """Learn IQR limits only on training inputs; cap AP_HI and AP_LO."""
    def __init__(self, columns=(4,5), factor=1.5):
        self.columns=columns
        self.factor=factor
    def fit(self,X,y=None):
        data=np.asarray(X,dtype=float)
        self.n_features_in_=data.shape[1]
        q1=np.quantile(data[:,self.columns],0.25,axis=0)
        q3=np.quantile(data[:,self.columns],0.75,axis=0)
        self.lower_=q1-self.factor*(q3-q1)
        self.upper_=q3+self.factor*(q3-q1)
        return self
    def transform(self,X):
        data=np.asarray(X,dtype=float).copy()
        data[:,self.columns]=np.clip(data[:,self.columns],self.lower_,self.upper_)
        return data
