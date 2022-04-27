from dataService import get_candidate_by_id, voted_candidate, vote_candidate, increase_votes, create_campaign, add_candidates


def vote(user, candidate_id):
    candidate = get_candidate_by_id(candidate_id)
    if len(candidate) == 0:
        return {'error': 'Invalid candidate id'}

    voted = voted_candidate(user)
    if 'error' not in voted.keys():
        return {'error': 'You can only vote for one candidate'}

    result = vote_candidate(user, candidate_id)
    if 'error' in result.keys():
        return result

    return increase_votes(candidate_id)


def create_new_campaign(creator, payload):
    try:
        if type(payload['candidates']) is not list:
            return {'error': 'Wrong input format'}

        campaign = create_campaign(creator, payload['description'],
                                   payload['start_time'], payload['end_time'], payload['name'])
        print(campaign)

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
