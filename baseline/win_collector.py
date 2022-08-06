import csv
import numpy as np
import pandas as pd
from tqdm import tqdm
import multiprocessing
from base64 import encode
import requests, string, time
from statistics import mean
from datetime import datetime
import logging
import json

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')


class DataCollector:
    """
    This is the base class for collecting the required data. The data is obtained
    via REST API's

    """

    def __init__(self, inference=False):
        # Specify if the data we are obtaining is for Inference or not
        self.inference = inference

    def get_clean_account_addresses(self):
        '''
        This method gets the clean account addresses
        '''
        logging.debug("Starting retrieval of clean accounts from Github")

        # Read CSV file on the Github repo
        clean_account_adresses = pd.read_csv(
            'https://raw.githubusercontent.com/Vagif12/Ethereum-Fraud-Detection/master/datasets/clean_adresses.csv')
        # logging.debug the number of unique and clean addresses
        logging.debug('Number of clean account adressess: ' + str(len(clean_account_adresses['Address'])))
        logging.debug(
            'Number of unique clean account adressess: ' + str(len(np.unique(clean_account_adresses['Address']))))

        # Return a numpy array of addresses obtained
        return np.array(clean_account_adresses['Address'])

    def get_illicit_account_addresses(self):
        '''
        This method gets the illictit account addresses via a supplementary JSON File

        '''

        # JSON File
        address_darklist = requests.get(
            'https://raw.githubusercontent.com/MyEtherWallet/ethereum-lists/master/src/addresses/addresses-darklist.json').json()
        addresses = []

        for item in address_darklist:
            addresses.append(item['address'])

        logging.debug("Number of illegal addresses: ", len(address_darklist))
        logging.debug("Number of unique illegal addresses in JSON file: ", len(np.unique(addresses)))

        return np.array(addresses)

    def main(self, name='combined_dataset'):
        """
        Main function of the DataCollector Class.
        This function links together all the methods and processes together

        Parameters:
        name = the name of the csv file to be saved
        inference_addresses = if inference=True, then the list of addresses to fetch data from
        """
        cleans = self.get_clean_account_addresses()
        illicits = self.get_illicit_account_addresses()

        index = 1
        pbar = tqdm(total=len(cleans)+len(illicits))

        # writing information for clean addresses
        for address in cleans:
            # Loop through addresses, and get data for each address
            print(address)
            try:
                # Save obtained data to csv file
                normal_txns = self.normal_transactions(index, address, flag=0)
                print("Information collected!")
                all_txns = normal_txns
                with open(r'./{}.csv'.format(name), 'a', newline="") as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(all_txns)
                    logging.debug(all_txns)
                print("Clean address #" + str(index) + " - " + address + " information written into CSV!")
                print(datetime.now())
                print("-----")
                index += 1
                pbar.update(1)
            except Exception as e:
                print("Error message: ")
                print(e)

        # writing information for illicit addresses
        for address in illicits:
            # Loop through addresses, and get data for each address
            print(address)
            try:
                # Save obtained data to csv file
                normal_txns = self.normal_transactions(index, address, flag=1)
                print("Information collected!")
                all_txns = normal_txns
                with open(r'./{}.csv'.format(name), 'a', newline="") as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(all_txns)
                    logging.debug(all_txns)
                print("Illicit address #" + str(index) + " - " + address + " information written into CSV!")
                print(datetime.now())
                print("-----")
                index += 1
                pbar.update(1)
            except Exception as e:
                print("Error message: ")
                print(e)

        pbar.close()

    def normal_transactions(self, index, address, flag):
        """
        Function to obtain data on normal_transactions

        Parameters:
        index: the index number to index the data
        address: the address of an account
        flag: whether the transactions are fraud(1) or not(0)

        Returns:
        transaction_fields = different features based on normal transactions
        """
        all_stamps, recipients, timeDiffSent, timeDiffReceived, receivedFromAddresses, \
        sentToAddresses, sentToContracts, valueSent, valueReceived, valueSentContracts = ([] for i in range(10))
        receivedTransactions, sentTransactions, createdContracts, minValReceived, \
        maxValReceived, avgValReceived, minValSent, maxValSent, avgValSent, minValSentContract, \
        maxValSentContract, avgValSentContract = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        transaction_fields = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        offset = 0
        limit = 500000

        while 1:

            URL = "http://128.32.43.220:8000/query?q=SELECT%20hash,block_timestamp,to_address,from_address,value%20FROM%20" \
                  "transactions%20WHERE%20from_address=%27{address}%27%20OR%20to_address=%27{address}%27%20ORDER%20BY%20" \
                  "block_timestamp%20LIMIT%20{limit}%20OFFSET%20{offset}".format(address=address,limit=limit,offset=offset*limit)
            r = requests.get(url=URL)
            print("request " + str(offset+1) + " retrieved")
            data = r.json()
            print("result " + str(offset+1) + " converted to json")

            if len(data['result']['hash']) < 2:
                break

            try:
                for tnx_num in range(len(data['result']['hash'])):
                    timestamp = data['result']['block_timestamp']['{tnx}'.format(tnx=tnx_num)]
                    all_stamps.append(timestamp)
                    # processing transactions sent to this address
                    if data['result']['to_address']['{tnx}'.format(tnx=tnx_num)] == address:
                        receivedTransactions = receivedTransactions + 1
                        receivedFromAddresses.append(data['result']['from_address']['{tnx}'.format(tnx=tnx_num)])
                        valueReceived.append(int(data['result']['value']['{tnx}'.format(tnx=tnx_num)]) / 1000000000000000000)
                        if receivedTransactions > 0:
                            t1 = datetime.strptime(all_stamps[len(all_stamps) - 1], "%Y-%m-%dT%H:%M:%S%z")
                            t2 = datetime.strptime(all_stamps[len(all_stamps) - 2], "%Y-%m-%dT%H:%M:%S%z")
                            timeDiffReceived.append(abs(int((t1 - t2).total_seconds())) / 60)
                    # processing transactions originating from this address
                    if data['result']['to_address']['{tnx}'.format(tnx=tnx_num)] == address:
                        sentTransactions = sentTransactions + 1
                        sentToAddresses.append(data['result']['to_address']['{tnx}'.format(tnx=tnx_num)])
                        valueSent.append(int(data['result']['value']['{tnx}'.format(tnx=tnx_num)]) / 1000000000000000000)
                        if receivedTransactions > 0:
                            t1 = datetime.strptime(all_stamps[len(all_stamps) - 1], "%Y-%m-%dT%H:%M:%S%z")
                            t2 = datetime.strptime(all_stamps[len(all_stamps) - 2], "%Y-%m-%dT%H:%M:%S%z")
                            timeDiffSent.append(abs(int((t1 - t2).total_seconds())) / 60)
            except Exception as e:
                print("Error in normal_transactions(): ")
                print(e)
                print(" at address: " + address)

            offset += 1

        totalTnx = sentTransactions + receivedTransactions + createdContracts
        totalEtherReceived = np.sum(valueReceived)
        totalEtherSent = np.sum(valueSent)
        totalEtherSentContracts = np.sum(valueSentContracts)
        totalEtherBalance = totalEtherReceived - totalEtherSent - totalEtherSentContracts
        avgTimeBetweenSentTnx = self.avgTime(timeDiffSent)
        avgTimeBetweenRecTnx = self.avgTime(timeDiffReceived)
        numUniqSentAddress, numUniqRecAddress = self.uniq_addresses(sentToAddresses, receivedFromAddresses)
        minValReceived, maxValReceived, avgValReceived = self.min_max_avg(valueReceived)
        minValSent, maxValSent, avgValSent = self.min_max_avg(valueSent)
        minValSentContract, maxValSentContract, avgValSentContract = self.min_max_avg(valueSentContracts)
        timeDiffBetweenFirstAndLast = self.timeDiffFirstLast(all_stamps)

        ILLICIT_OR_NORMAL_ACCOUNT_FLAG = flag

        transaction_fields = [index, address, ILLICIT_OR_NORMAL_ACCOUNT_FLAG, avgTimeBetweenSentTnx,
                              avgTimeBetweenRecTnx, timeDiffBetweenFirstAndLast,
                              sentTransactions,
                              receivedTransactions, createdContracts,
                              numUniqRecAddress, numUniqSentAddress,
                              minValReceived, maxValReceived, avgValReceived,
                              minValSent, maxValSent, avgValSent,
                              minValSentContract, maxValSentContract, avgValSentContract,
                              totalTnx, totalEtherSent, totalEtherReceived, totalEtherSentContracts,
                              totalEtherBalance]

        return transaction_fields

    def timeDiffFirstLast(self, timestamps):
        """
        This function calculates the time difference from last transaction

        Parameters:
        timestamp: an array of the timestamps of all the transactions related to one address

        Returns:
        timeDiff: the calculated time difference between the first and last transaction
        """
        time_diff = 0
        if len(timestamps) > 0:
            t1 = datetime.strptime(timestamps[0], "%Y-%m-%dT%H:%M:%S%z")
            t2 = datetime.strptime(timestamps[-1], "%Y-%m-%dT%H:%M:%S%z")
            time_diff = "{0:.2f}".format(abs(int((t1 - t2).total_seconds())) / 60)

        return time_diff

    def avgTime(self, timeDiff):
        """
        This function calculates the average time from the time difference

        Parameters:
        timestamp: the time difference of a transaction

        Returns:
        timeDiff: the calculated average time
        """
        avg = 0
        if len(timeDiff) > 1:
            avg = "{0:.2f}".format(mean(timeDiff))
        return avg

    def min_max_avg(self, value_array_tnxs):
        """
        This function calculates the minimum and maximum average time from the transactions

        Parameters:
        value_array_tnxs: an array of transactions

        Returns:
        the minimum, maximum and avg transaction time
        """
        minVal, maxVal, avgVal = 0, 0, 0
        if value_array_tnxs:
            minVal = min(value_array_tnxs)
            maxVal = max(value_array_tnxs)
            avgVal = mean(value_array_tnxs)
        return "{0:.6f}".format(minVal), "{0:.6f}".format(maxVal), "{0:.6f}".format(avgVal)

    def uniq_addresses(self, sent_addresses, received_addresses):
        """
        This method calculates the number of unique addresses sent and received

        Parameters:
        sent_addresses = an array of addresses that transactions were sent to
        received_addresses = an array of addreses that transactions were received from

        Returns:
        uniqSent = number of unique sent addresses
        uniqRec = number of unique received addresses
        """
        uniqSent, createdContrcts, uniqRec = 0, 0, 0
        if sent_addresses:
            uniqSent = len(np.unique(sent_addresses))

        if received_addresses:
            uniqRec = len(np.unique(received_addresses))
        return uniqSent, uniqRec
