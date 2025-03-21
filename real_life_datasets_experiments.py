from src.BatchFileLoader import BatchFileLoader
from src.Evaluator import MultiEvaluator
from src.Filtering import Filtering
import os

INPUT_DIR = "./real_life_datasets/"
OUTPUT_DIR = "./real_life_datasets_results/" 
METHODS = ["Genetic Miner", "Inductive Miner"]
NUM_WORKERS = 1

if __name__ == "__main__":
    dataset_dirs = os.listdir(INPUT_DIR)
    dataset_dirs = [x for x in dataset_dirs if not os.path.isfile(f"{INPUT_DIR}{x}")]
    eventlogs = {} # name: eventlog
    loader = BatchFileLoader(cpu_count=NUM_WORKERS)
    
    for dataset_dir in dataset_dirs:
        temp_eventlogs = loader.load_all_eventlogs(f"{INPUT_DIR}{dataset_dir}")
        
        # check that there is only one event log in the directory
        assert len(temp_eventlogs) == 1, f"Expected one event log in {dataset_dir}, got {len(temp_eventlogs)}"
        for eventlog in temp_eventlogs.values():
            eventlog = Filtering.filter_eventlog_by_top_percentage_unique(eventlog, 0.1)
            eventlogs[dataset_dir] = eventlog
    
    #Create and evaluate the MultiEvaluator
    multi_evaluator = MultiEvaluator(
        eventlogs, 
        methods=METHODS,
        random_creation_rate=0.2,
        crossover_rate=0.2,
        mutation_rate=0.3,
        elite_rate=0.3,
        min_fitness=None,
        max_generations=200,
        stagnation_limit=80,
        time_limit=None,
        population_size=100
    )
    
    results_df = multi_evaluator.evaluate_all(num_cores=NUM_WORKERS)
    multi_evaluator.save_df_to_pdf(results_df, OUTPUT_DIR + "results.pdf")
    multi_evaluator.export_petri_nets(OUTPUT_DIR)