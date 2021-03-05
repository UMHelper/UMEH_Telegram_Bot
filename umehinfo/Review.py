class Review:
    def __init__(self,result:dict):
        self.content=result['content']
        self.grade=result['grade']
        self.attendance=result['attendance']
        self.hard=result['hard']
        self.reward=result['reward']
        self.pre=result['pre']
        self.recommend=['recommend']
        self.assignment=result['assignment']
        self.upvote=result['upvote']
        self.downvote=result['downvote']
        self.pub_time=['pub_time']
