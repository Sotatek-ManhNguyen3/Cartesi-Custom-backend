import datetime

from dataService import get_candidate, voted_candidate, vote_candidate, increase_votes, create_campaign, \
    add_candidates, get_campaign, update_time_campaign


def vote(user, candidate_id, campaign_id):
    # Validate campaign and valid time to vote
    campaign = get_campaign(campaign_id)

    if len(campaign) == 0:
        return {'error': 'Campaign does not exist'}

    campaign = campaign[0]
    start_time = get_date_time_from_string(campaign['start_time'])
    end_time = get_date_time_from_string(campaign['end_time'])
    now = datetime.datetime.now()
    if now.__lt__(start_time) or now.__gt__(end_time):
        return {'error': 'This campaign is closed for voting'}

    # Validate candidate
    candidate = get_candidate(candidate_id, campaign_id)
    if len(candidate) == 0:
        return {'error': 'Invalid candidate id'}

    # Validate voted candidate
    voted = voted_candidate(user, campaign_id)
    if 'error' not in voted.keys():
        return {'error': 'You can only vote for one candidate'}

    # Vote
    result = vote_candidate(user, candidate_id, campaign_id)
    if 'error' in result.keys():
        return result

    # Increase vote in candidates table
    return increase_votes(candidate_id, campaign_id)


def get_date_time_from_string(time):
    time = time.split(' ')
    time = time[0].split('-') + time[1].split(':')
    return datetime.datetime(*[int(x) for x in time])


def create_new_campaign(creator, payload):
    try:
        if type(payload['candidates']) is not list:
            return {'error': 'Wrong input format'}

        campaign = create_campaign(creator, payload['description'],
                                   payload['start_time'], payload['end_time'], payload['name'])

        if 'error' in campaign.keys():
            return {'error': campaign}

        candidates = []
        for candidate in payload['candidates']:
            candidates.append([
                candidate['name'],
                campaign['id'],
                candidate['avatar'] if 'avatar' in candidate.keys() else '',
                candidate['brief_introduction'] if 'brief_introduction' in candidate.keys() else '',
            ])

        add_candidates(candidates)
        return campaign
    except KeyError as e:
        result = "EXCEPTION: " + e.__str__()
        print("NOTICE EXCEPTION" + e.__str__())
        return {'error': result}


def get_voted_candidate(user, campaign_id):
    campaign = get_campaign(campaign_id)
    if len(campaign) == 0:
        return {'error': 'Campaign does not exist'}

    return voted_candidate(user, campaign_id)


def change_time_campaign(user_change, campaign_id, start_time, end_time):
    campaign = get_campaign(campaign_id)
    if len(campaign) == 0:
        return {'error': 'Campaign does not exist!'}

    if campaign[0]['creator'] != user_change:
        return {'error': 'You do not have the permission!'}

    return update_time_campaign(campaign_id, start_time, end_time)
