import argparse as arg

def init_argparser():
    
    # Description
    logo ="""                                                                             
    xx  N|N|N|N|N|N|N|N|N|N|N|N|N|N|N|N|N|H|H|H|H|H|H|H|H|H|H|H|H|H|H|H|H|H|H|   xx
    ++  ----------------------------------------------------------------------   --
    ++    _                         _                       _                    --
    ++   /_/|                    _ /_/|_                  /_/|                    --
   ++   | | |_     _ _    _ _   /_|  |__/|  _ _ _    _ _ | | |_    _ _ _  _ _      --
  ++    | |_ _/\ / _ _/\ /_ _/\|__    __|/ /_ _ _/| / _ /| |_ _/\/ _ _/_/'_ _/|   --
   ++   |  _  \ |  __ \//  _  \ | |  | |  /   _ _|/  _  \|  _  \/  __ \ ' _ _|/  --
    ++  | |_|  ||  ___/|  |_|  || |  | |  \_ _   \  |_|  | |_|  |  ___/  | |     --
    ++  |_  _ //|_ _ _|/\ _ _,_|/ |__|/   /_ _ _ /\ _ _,_|_  _ / \ _ _|_ |/       --
   ++   ______________________________________________________________________    --
  ++     // // // // // // // // // // // // // // // // // // // // // // //    --
    xx  =======================================================================  xx
    """



    print(logo)

    # Create parser object
    parser = arg.ArgumentParser()
    

    # Insert camera number option
    parser.add_argument("-c","--camera", help="define the camera to use", type= int)

    # Make the system more verbose
    parser.add_argument("-v","--verbose", help = "display all messages", action="store_true")

    parser.parse_args()
    args = parser.parse_args()

    if(args.verbose):
        print(f"Camera number {args.camera} is being used ...")
    
    return args



# Debug main loop
if __name__ == "__main__":
    print("Argument parsing module test...\n")
    init_argparser()
