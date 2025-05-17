from trading_bot.components.data_ingestion import DataIngestionComponents
from trading_bot.configuration import DataIngestionConfig


class DataIngestionPipeline:
    
    def run(self, uploaded_files):
        # data ingestion
        self.data_ingestion=DataIngestionComponents(DataIngestionConfig)
        self.data_ingestion.main(uploaded_files)

