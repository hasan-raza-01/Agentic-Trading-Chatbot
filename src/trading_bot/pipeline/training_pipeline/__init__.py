from trading_bot.components.data_ingestion import DataIngestionComponents
from trading_bot.configuration import DataIngestionConfig
from dataclasses import dataclass 


@dataclass 
class TrainingPipeline:
    
    def run(self, uploaded_files):
        # data ingestion
        self.data_ingestion=DataIngestionComponents(DataIngestionConfig)
        self.run(uploaded_files)

