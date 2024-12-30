import csv
import pycountry

from linkedin_api import Linkedin

def main():
    linkedin = Linkedin('mistix515new@gmail.com', '99nUr3EX5JGfj6!')

    if linkedin:
        print("Logged successfully!")
    
    companies = linkedin.search_companies(keywords=['bot development'], limit=-1)
    
    with open('bot_development.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, 
                                fieldnames=['name', 'tagline', 'lnkd_url', 'company_url', 'country', 'staff_count', 'follower_count', 'specialities'],
                                delimiter=',',
                                lineterminator='\n')
        
        writer.writeheader()
        
        print("Start scraping")
        
        print(f"Total companies pages found: {len(companies)}")

        for count, company in enumerate(companies):
            id = company.get('urn_id')

            try:
                profile_info = linkedin.get_company(id)
            
            except Exception as e:
                print(f"Can't get profile info: {e}")
                continue

            if 'headquarter' in profile_info:
                country = profile_info['headquarter'].get('country', 'N/A').strip()

                if country in ["US", "UK", "UA", "IL", "CH", "CZ", "PL", "HR", "ES"]:
                    try:
                        styled_country = pycountry.countries.get(alpha_2=country).name
                    except Exception:
                        styled_country = country             
                else:
                    continue

            else:
                country = 'N/A'

            if 'tagline' in profile_info:
                tagline = profile_info['tagline'].strip()
            else:
                tagline = 'N/A'

            if 'companyPageUrl' in profile_info:
                company_url = profile_info['companyPageUrl'].strip()
            else:
                company_url = 'N/A'

            if not profile_info['followingInfo'].get('followerCount') > 100:
                continue
        
            if profile_info['staffCount'] > 15:
                continue

            writer.writerow({
                'name': profile_info['name'].strip(),
                'tagline': tagline,
                'lnkd_url': profile_info['url'].strip(),
                'company_url': company_url,
                'country': styled_country,
                'staff_count': profile_info['staffCount'],
                'follower_count': profile_info['followingInfo'].get('followerCount'),
                'specialities': profile_info['specialities'][:3]
            })

            print(f"Scraped: {count}", end='\r')
    print("Scraping finished!")
    
if __name__ == '__main__':
    main()