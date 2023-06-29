import pandas as pd
from typing import Optional
from pydantic import BaseModel
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error

class Model(BaseModel):
    """
    This class is used to store the model and its parameters.
    Attributes:
        name (str): The name of the model.
        model (object): The model to be used.
        params (dict): The parameters of the model.
        grid_search (bool): Whether to use grid search or not.
    """
    name: str
    model: object
    params: dict = {}
    grid_search: bool = True

class ModelEvaluator(BaseModel):
    """
    This class is used to evaluate the model.
    Attributes:
        model (Model): The model to be evaluated.
        cv (int): The number of folds to be used in cross validation.
        n_jobs (int): The number of jobs to be used in cross validation.
        best_params (dict): The best parameters of the model.
        sq_error (float): The mean squared error of the model.
        abs_error (float): The mean absolute error of the model.
    """
    model: Model
    cv: int = 5
    n_jobs: int = -1
    best_params: dict = {}
    sq_error: float = 0.0
    abs_error: float = 0.0

    class Config:
        arbitrary_types_allowed = True

    def fit(self, X_train:pd.DataFrame, y_train:pd.Series):
        if self.model.grid_search:
            self.model.model = GridSearchCV(
                self.model.model, 
                self.model.params, 
                cv=self.cv, 
                n_jobs=self.n_jobs)
            self.model.model.fit(X_train, y_train)
            self.best_params = self.model.model.best_params_
        return self.model.model.best_estimator_

    def predict(self, X_test:pd.DataFrame):
        return self.model.model.predict(X_test)
    
    def evaluate(
            self,
            X_train:pd.DataFrame,
            y_train:pd.Series,
            X_test:pd.DataFrame,
            y_test:pd.Series):
        
        self.model.model = self.fit(X_train, y_train)
        y_pred = self.predict(X_test)
        self.sq_error = mean_squared_error(y_test, y_pred)
        self.abs_error = mean_absolute_error(y_test, y_pred)

        print("Model: %s" % self.model.name)
        print("Best params: %s" % self.best_params)
        print("Mean Square Error: %.2f" % 
              self.sq_error)
        print("Mean Absolute Error: %.2f" % 
              self.abs_error)