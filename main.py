import message_indexer
import message_parser
import message_querer


def main():
    jsonData = message_parser.message_parser()
    message_parser.fix_encoding(jsonData)
    message_indexer.message_indexer(jsonData)
    message_querer.query_aggregate_data_from_db()

if __name__ == "__main__":
    main()
