import numpy as np

class AffinityPropagation:
    def __init__(self, org_matrix) -> None:
        self.org_matrix = org_matrix
        self.org_matrix_len = len(org_matrix)

    def find_clusters(self):
        return self.__find_similarity_matrix()

    def __find_similarity_matrix(self): 
        sim_matrix = np.zeros((self.org_matrix_len, self.org_matrix_len), dtype=int)
        
        for i in range(len(self.org_matrix)):
            for j in range(len(self.org_matrix)):
                sim_matrix[i, j] = - sum((self.org_matrix[i] - self.org_matrix[j]) ** 2)

        for i in range(len(self.org_matrix)):
            for j in range(len(self.org_matrix)):
                if i == j:
                    sim_matrix[i, j] = sim_matrix.min() 

        return self.__find_responsibility_matrix(sim_matrix)

    def __find_responsibility_matrix(self, sim_matrix):
        responsibility_matrix = np.zeros((self.org_matrix_len, self.org_matrix_len), dtype=int)    

        for i in range(self.org_matrix_len):
            for j in range(self.org_matrix_len):
                row_excludng = (sim_matrix[i, :j], sim_matrix[i, j+1:])
                row_excludng_max = max(np.concatenate(row_excludng))
                responsibility_matrix[i, j] = sim_matrix[i, j] - row_excludng_max
                
        return self.__find_availibilty_matrix(responsibility_matrix)

    def __find_availibilty_matrix(self, responsibility_matrix):
        avail_matrix = np.zeros((self.org_matrix_len, self.org_matrix_len), dtype=int)   

        for i in range(self.org_matrix_len):
            for j in range(self.org_matrix_len):
                if i == j: 
                    col_exclud = (responsibility_matrix[:i, j], responsibility_matrix[i:, j])
                    col_exclud = np.concatenate(col_exclud)
                    avail_matrix[i, j] = np.int64((col_exclud +  np.abs(col_exclud)).sum()/2)
                else:
                    exclude = (responsibility_matrix[:i, j], responsibility_matrix[i:, j])
                    exclude = np.concatenate(exclude)
                    if len(exclude) > 1:
                        subs = np.zeros((len(exclude)), dtype=int)
                        subs[i], subs[j] = responsibility_matrix[i,j], responsibility_matrix[j,j]
                    col_exclud = exclude - subs
                    inclusion =  responsibility_matrix[j,j] + np.int64((col_exclud +  np.abs(col_exclud)).sum()/2)
                    avail_matrix[i,j] = min([0, inclusion]) 
                
        return self.__find_criterion_matrix(responsibility_matrix, avail_matrix)

    def __find_criterion_matrix(rself, responsibility_matrix, avail_matrix):
        return responsibility_matrix + avail_matrix
