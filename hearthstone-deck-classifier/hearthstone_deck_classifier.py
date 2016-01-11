import Classifiers
import csv

decks_file = "hearthstonedecks.csv"
raw_data = []

test_filte = "test.csv"
test_data = []

def LoadDataset(filename, data=[], keys=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        keys = dataset[0]
        for x in range(1, len(dataset)):
            element = {}
            for y in range(len(dataset[x])):
                element[keys[y]] = dataset[x][y]
            data.append(element)

def main():
    LoadDataset(decks_file, raw_data)
    LoadDataset(test_filte, test_data)
    
    naive_bayes = Classifiers.NaiveBayes()
    naive_bayes.ProcessData(raw_data)

    expected = naive_bayes.Classify(test_data[0]["class"], test_data)

    print(expected)
    print(test_data[0]["archetype"])

    print('Hello World')


if __name__ == "__main__":
    main()