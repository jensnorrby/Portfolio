import logging
import matplotlib.pyplot as plt
import argparse
import stocks


def setup_logger():
    logging.basicConfig(
        filename="main.log",
        format="[%(levelname)s] %(asctime)s : %(message)s",
        encoding="utf-8",
        level=logging.INFO,
    )


def main(args):
    db = stocks.StocksDB("data")
    
    if args.plot:
        # INSERT CODE HERE #
        pass

    elif args.candle:
        # INSERT CODE HERE #
        pass

    elif args.table:
         
    #I create a Table object and gives the args as arguments.
        table = stocks.Table(db)
        table.print(args.table, args.limit)


if __name__ == "__main__":
    setup_logger()

    # -------------------------------------
    # Command line input parser
    # -------------------------------------
    arg_parser = argparse.ArgumentParser()
    # INSERT CODE HERE #
    # add start/end aguments
    # add table/limit arguments
    # add plot/candle arguments
    arg_parser.add_argument("--table", type=str, help="Prints a table with stock values over time sorted by the given metric.")
    arg_parser.add_argument("--limit", type=int, help="Limit the number of stocks to the top n entries.")
    # -------------------------------------
    args = arg_parser.parse_args()
    # -------------------------------------
    logging.info(f"Started running main.py: args: {args}")
    # -------------------------------------

    main(args)
