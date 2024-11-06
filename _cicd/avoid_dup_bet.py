# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    avoid_dup_bet.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: umeneses <umeneses@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/06 08:12:15 by umeneses          #+#    #+#              #
#    Updated: 2024/11/06 08:25:53 by umeneses         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def check_duplicates_bets(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    
    seen = {}
    for line_number, line in enumerate(lines, start=1):
        if line in seen:
            print(f"Duplicated BET found on line {line_number}: '{line}'")
            sys.exit(line_number)
        seen[line] = line_number

    print("No duplicates found.")
    sys.exit(0)

if __name__ == "__main__":
    check_duplicates_bets('../blocklist.txt')

