# backend_api/services/case_service.py

class CaseService:
    def __init__(self, repo):
        self.repo = repo

    def create_case(self, title, description, status):
        # Rules can stay here later
        return self.repo.create(title, description, status)
    
    def get_case(self, case_id):
        return self.repo.get_by_id(case_id)
    
    def update_case(self, case_id, title, description, status):
        return self.repo.update(case_id, title, description, status)
    
    def delete_case(self, case_id):
        return self.repo.delete(case_id)