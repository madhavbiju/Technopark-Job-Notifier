from dataclasses import dataclass
from typing import Optional

@dataclass
class Company:
    id: int
    name: str
    logo: Optional[str]

@dataclass
class Job:
    id: int
    job_listing_id: str
    job_title: str
    posted_date: str
    closing_date: Optional[str]
    company: Company

    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        company_data = data.get('company', {})
        company = Company(
            id=company_data.get('id', 0),
            name=company_data.get('company', 'Unknown Company'),
            logo=company_data.get('logo')
        )
        return cls(
            id=data.get('id', 0),
            job_listing_id=data.get('job_listing_id', ''),
            job_title=data.get('job_title', ''),
            posted_date=data.get('posted_date', ''),
            closing_date=data.get('closing_date'),
            company=company
        )
