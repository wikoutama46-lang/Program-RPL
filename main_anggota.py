from views.anggota_view import AnggotaView
from models.anggota_model import AnggotaModel
from controllers.anggota_controller import AnggotaController

if __name__ == "__main__":
    app = AnggotaView()
    model = AnggotaModel()
    controller = AnggotaController(app, model)
    app.mainloop()