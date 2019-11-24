import requests
import json
from tqdm import tqdm as tqdm

def item_data_extracter(id_list, acceptable_types=['story'], score_threshold = None, out_path = None):
    """
    Function will extract data on Hackernews items. Data can include stories, comments, asks, jobs and polls.
    When item is a story, data includes; post date, poster, children, title and url.

        Args:
            `id_list` - List: HackerNews Item IDs to pull data from.
            `acceptable_types` - List: Program will filter out items of types not included
                in this list. Other options include:
                'story', 'comment', 'ask', 'job', 'poll', 'pollopt' (poll option)
            `score_threshold` - Int: If not None, items below this threshold will be filtered from results.
                No filtering if `score_threshold` == None.
            `out_path` - Str: Path to save results to. Will attempt to load file and append to its data if necessary.

        Returns:
            `pre_existing_data` - Dict: Updated version of the loaded pre-exisiting-data dictionary.
    """
    ### Check if file exists at `out_path` and load data from it.
    try:
        ### If it exists, load the data to `pre_existing_data`
        with open(f'{out_path}.json', 'r') as f:
            pre_existing_data = json.load(f)
        print('Loaded pre-existing data.')
    except:
        ### If it doesn't exist, load a blank dict to `pre_existing_data`
        pre_existing_data = dict()
        print('No pre-existing data.')

    ### Filter input ID list based on item ids in `pre_exisiting_data`
    id_list = [i for i in id_list if str(i) not in pre_existing_data.keys()]
    if len(id_list) == 0:
        id_list = ['1']
    items_dict = {}
    for item_id in tqdm(id_list, total=len(id_list)):
        item_dict = {}
        item_url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty'
        item_text = requests.get(item_url).text

        ### Replace `'` with `\"` for the json decoder
        json_acceptable_string = item_text.replace("'", r"\"")
        try:
            item_dict = json.loads(json_acceptable_string)#.decode('utf-8')
        except json.JSONDecodeError as e:
            ### If json.loads() fails, print the error and the string to allow
            ### debugging of the output.
            ### Ideally, add a replace to the item_text.replace() row above with the error causing character
            print(e)
            print(json_acceptable_string)
            return {}
        ### Check if the item fits the acceptable_types constraints
        if (acceptable_types[0] is not None) and (item_dict['type'] not in acceptable_types):
            continue
        ### Check if the item fits the score_threshold constraints
        if (score_threshold is not None) and (story_dict['score'] < score_threshold):
            continue
        ### If the item matches all the constraints, add it to the output data
        items_dict.update({item_id : item_dict})

    ### Update the pre-exisiting data with the newly pulled rows
    pre_existing_data.update(items_dict)

    ### Write output
    with open(f'{out_path}.json', 'w') as fout:
        json.dump(pre_existing_data, fout, indent = 4)

    return pre_existing_data



def btn_stories_data_extraction(stories_type='best', results=None, acceptable_types = ['story']):
    """
    This function allows users to pull either the best, top and new stories from Hackernews.

        Args:
            `stories_type` - Str: Value determines the type of stories to pull.
                Options include: ['best', 'top', 'new']
            `results` - Int: Value determines the number of results returned. Leaving default value
                will pull all results (500).
            `acceptable_types` - List: Parameter will be passed to `item_data_extracter()`.
                Program will filter out items of types not included in this list.
                Other options include:
                    'story', 'comment', 'ask', 'job', 'poll', 'pollopt' (poll option)
    """
    btn_url = f'https://hacker-news.firebaseio.com/v0/{stories_type}stories.json?print=pretty'

    url_text = requests.get(btn_url).text
    url_ids = url_text.replace('[ ', '').replace(' ]\n', '').split(', ')
    btn_storys_dict = {}
    if results == None:
        btn_storys_dict = item_data_extracter(id_list = url_ids, acceptable_types = acceptable_types)
    else:
        print(url_ids[:results])
        btn_storys_dict = item_data_extracter(id_list = url_ids[:results], acceptable_types = acceptable_types)

    return btn_storys_dict



for i in range(1, 1000000, 10000):
    item_data_extracter(id_list = range(i, i + 10000), acceptable_types = ['story', 'comment'], out_path = 'hn_json')
