import challonge
import json
import argparse

parser = argparse.ArgumentParser(description='Demande a notre ami Bob de creer une semaine BYOS.')
parser.add_argument("-s", "--saison", help="L'identifiant de la saison")
parser.add_argument("-w", "--semaine", help="L'identifiant de la semaine")

args = parser.parse_args()
url_root = "byos_TEST"

if not args.saison or not args.semaine:
    print(parser.print_help())
    raise Exception("Saison ou semaine non specifiee")


def create_tournament(saison, semaine, groupe, players):

    url = url_root+saison+"_"+semaine+"_"+groupe
    challonge.tournaments.create("BYOS S"+saison+" Sem. "+semaine+" Grp. "+groupe, url,
                                 "round robin", open_signup=False, ranked_by="points difference")

    for player in players:
        challonge.participants.create(url, player)


def create_week(saison, semaine, groupes):
    cpt = 1
    for groupe in groupes:
        create_tournament(saison, semaine, str(cpt), groupe)
        cpt += 1


with open('credentials_test.json') as f:
    creds = json.load(f)

with open('groupes.json') as f:
    tab_groupes = json.load(f)["groupes"]

challonge.set_credentials(creds["username"], creds["api_key"])

create_week(str(args.saison), str(args.semaine), tab_groupes)
