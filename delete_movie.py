from configs.config import CONFIG, db

if __name__ == '__main__':
    print('Deleted {} movies.'.format(db.movie.delete_many({}).deleted_count))
    print('Deleted {} schedules.'.format(db.schedule.delete_many({}).deleted_count))
    print('Deleted {} candidates.'.format(db.candidate.delete_many({}).deleted_count))