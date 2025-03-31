#!/usr/bin/env python3

#import modules
import os
import statistics
from argparse import ArgumentParser
import glob

#parse arguments for future run
def make_parser():
    parser = ArgumentParser(description="Split the input file into smaller files of roughly equal size.")
    parser.add_argument("file_path", help="path to the file to split")
    parser.add_argument("output_path", help="output directory to write new files.")
    parser.add_argument("--include-header", action="store_true", help="to add header in the output files. Not including headers by default", default=False)
    parser.add_argument("--threshold", type=int, help="maximum number of rows per new file. Default 50000", default=50000, required=False)
    parser.add_argument("--max_size", type=int, help="maximum file size in MB. Default 10 MB", default=10, required=False)
    return parser
    
def file_info(file_path):
    name, extension = os.path.basename(file_path).split('.')
    input_size = os.stat(file_path).st_size
    if extension == 'csv':
        delimiter = ','
    elif extension == 'tsv':
        delimiter = '\t'
    return(name, extension, delimiter, input_size)

def read_input(file_path, delimiter):
    article_rows = {}
    article_text = {}
    row_count = -1

    with open(file_path, "r") as f:
        for line in f:
            if row_count > -1:
                id = line.split(delimiter, maxsplit=1)[0]
                #create or add to list?
                if id in article_rows:
                    article_rows[id] += 1
                    article_text[id].append(line)
                else:
                    article_rows[id] = 1
                    article_text.setdefault(id, [])
                    article_text[id].append(line)
                    row_count += 1
            else:
                header_text = line
                row_count += 1
    
    #sorted dict by value
    article_rows = dict(sorted(article_rows.items(), key=lambda item: item[1]))
    print(f'Read file {file_path}')
    return(article_rows, article_text, header_text, row_count)

def batching(article_rows, input_size, row_count, threshold, max_size):
    #maximum rows write to a file
    max_rows_article = max(article_rows.values())
    median_rows_article = int(statistics.median(article_rows.values()))
    #size
    min_files = (input_size//(max_size*1024*1024)) + 1
    max_rows_in_a_file = row_count//min_files -1
    #max rows to write
    if median_rows_article < 2 or max_rows_article < 2:
        upper_row_level = min([max_rows_in_a_file, threshold+1])
    else:
        upper_row_level = min([max_rows_article, max_rows_in_a_file, threshold+1])
    ##print(f'Max rows in a file: {upper_row_level}')

    output_file_end = 0
    sum_values = 0
    articles_to_files ={}

    for key, value in article_rows.items():
        sum_values += value
        if sum_values >= upper_row_level:
            output_file_end += 1
            articles_to_files[key] = output_file_end
        else:
            articles_to_files[key] = output_file_end
    print(f'Creating {output_file_end} output files')
    return(articles_to_files)

def write_to_multiple_files(output_path, name, extension, articles_to_files, article_text, header, header_text):
    file_list = glob.glob(f"{output_path}/{name}-output-*.{extension}")
    if file_list:
        for filepath in file_list:
            os.remove(filepath)
    for key, value in articles_to_files.items():
        file_name = f"{output_path}/{name}-output-{value}.{extension}"
        with open(file_name, 'a') as file:
            if os.stat(file_name).st_size == 0 and header:
                file.write(header_text)
            for i in article_text[key]:
                file.write(i)
    print(f'Writing to {output_path}')


def main():
    parser = make_parser()
    args = parser.parse_args()
    print(f"solution {'--threshold' if args.threshold else ''} {args.threshold} {'--include-header' if args.include_header else ''} {args.file_path} {args.output_path}")
    name, extension, delimiter, input_size = file_info(args.file_path)
    article_rows, article_text, header_text, row_count = read_input(args.file_path, delimiter)
    articles_to_files = batching(article_rows, input_size, row_count, args.threshold, args.max_size)
    write_to_multiple_files(args.output_path, name, extension, articles_to_files, article_text, args.include_header, header_text)

if __name__ == "__main__":
    main()