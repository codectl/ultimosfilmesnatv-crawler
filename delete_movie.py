from configs.config import CONFIG, db
import argparse

if __name__ == '__main__':
    # print('Deleted {} movies.'.format(db.movie.delete_many({}).deleted_count))
    # print('Deleted {} schedules.'.format(db.schedule.delete_many({}).deleted_count))
    # print('Deleted {} candidates.'.format(db.candidate.delete_many({}).deleted_count))
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("sapo_id", nargs='?', default="check_string_for_empty")
    args = parser.parse_args()

    if args.sapo_id == 'check_string_for_empty':
        print('No argument given for sapo_id')
    else:
        db.movie.delete_many({'sapo_id': args.sapo_id})
        db.candidate.delete_many({'sapo_id': args.sapo_id})
        db.schedule.delete_many({'sapo_id': args.sapo_id})
