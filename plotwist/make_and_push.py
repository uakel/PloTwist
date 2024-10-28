"""
Invokable module that runs a report making script and pushes the report to a remote server
in regular intervals.
"""

import subprocess as sp

def make_and_push(script: str, scp_dest: str) -> None:
    """
    Runs a report making script and pushes the report to a remote server.
    """
    print(f"Running {script}...")
    sp.run(['python', script])
    print("Pushing report...")
    sp.run(['scp', '-r', 'report', scp_dest])
    print("done")

if __name__ == '__main__':
    import argparse
    import time
    import tqdm
    parser = argparse.ArgumentParser()
    parser.add_argument(type=str,
                        help='script to run',
                        dest='script')
    parser.add_argument(type=str, 
                        help='scp destination e.g. (user@host:/path/to/dest)',
                        dest='scp'
                        )
    parser.add_argument('--interval',
                        type=int,
                        default=60,
                        help='push interval in seconds')
    args = parser.parse_args()
    while True:
        make_and_push(args.script, args.scp)
        print("Waiting...")
        for _ in tqdm.tqdm(range(args.interval)):
            time.sleep(1)

    


