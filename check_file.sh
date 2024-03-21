#!/bin/bash
# STOCK='CVX'
# INPUT_PARAMETER="RET  VOL_CHANGE  BA_SPREAD  ILLIQUIDITY sprtrn TURNOVER DJI_Return"
# EXAMM="/home/zl7069/git/debug/exact"
RESULT_PATH="/Users/zimenglyu/Documents/cluster_results/DJI_Company_2022"
MAX_GENOME=20000
NUM_ISLAND=20
lr=0.0001
offset=1
SIZE_THRESHOLD=7 
# for STOCK in 'AAPL' 'AXP' 'BA' 'CAT' 'CSCO' 'CVX' 'DOW' 'DIS' 'WBA' 'GS' 'HD' 'IBM' 'INTC' 'JNJ' 'JPM' 'KO' 'MCD' 'MMM' 'MRK' 'MSFT' 'NKE' 'HON' 'PG' 'TRV' 'UNH' 'AMGN' 'VZ' 'V' 'WMT' 'CRM'
for STOCK in 'TRV'

do
    for folder in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 
    do
        exp_name="$RESULT_PATH/${STOCK}/lr_$lr/max_genome_$MAX_GENOME/island_$NUM_ISLAND/$folder"
        FILE_PATH="$exp_name/fitness_log.csv"
        # echo "Checking the file: "$FILE_PATH

        FILE_SIZE_BYTES=$(stat  -f %z "$FILE_PATH")
        FILE_SIZE_MB=$(echo "scale=2; $FILE_SIZE_BYTES / 1048576" | bc)

        # Compare the file size with the threshold
        if (( $(echo "$FILE_SIZE_MB < $SIZE_THRESHOLD" | bc -l) )); then
            echo "File is below the threshold size. Erasing the directory..."
            rm -rf "$exp_name"
            echo "Directory erased."$exp_name
        # else
        #     echo "File size is above the threshold. No action taken."
        fi

    done
done
