from NeuralEngine import Trainer, Predictor

T = Trainer()
T.train_all_and_save(filename="german.xlsx", epochs=30, batch_size=5)
#P = Predictor()
#op = P.predict(status_of_account="A11", duration="6", history="A34", purpose="A43", amount="1169", saving_bonds="A65",
#               employment="A75", rate="4",
#               status_sex="A93", other_coap="A101", resi_since="4", property="A121", age="67", other_plans="A143",
#               housing="A152",
#               existing_credits="2", job="A173", liability="1", telephone="A192", foreign="A201")
#print(op)