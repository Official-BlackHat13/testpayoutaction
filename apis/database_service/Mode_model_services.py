from ..database_models.ModeModel import ModeModel

class Mode_Model_Service:
    def __init__(self,mode):
        self.mode=mode
    def save(self):
        modemodel = ModeModel()
        modemodel.mode=self.mode
        modemodel.save()
    @staticmethod
    def fetch_by_id(id):
        modemodel = ModeModel.objects.get(id=id)
        return modemodel
    @staticmethod
    def fetch_by_mode(mode)->ModeModel:
        modemodel=ModeModel.objects.filter(mode=mode)
        if len(modemodel)==0:
            return None
        return modemodel[0]
