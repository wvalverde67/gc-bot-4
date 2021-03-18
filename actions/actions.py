from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List, Type, Union
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType


import requests
from requests.auth import HTTPBasicAuth

import json

class PromesaPagoFormValidator(FormValidationAction):
    def name(self) -> Text:
        return "promesa_pago_form"

    def validate_promesa_pago_form(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        return {
            "fecha_promesa_confirmada": slot_value,
            "lugar_pago":slot_value
            }

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def fetch_slots(tracker: Tracker) -> List[EventType]:
        """Trae del WebHook los datos de la promesa de pago."""

        
        response = requests.get('http://10.123.0.25/webApi/api/obtenerpromesa')
        promesa_pago = json.loads(response.content)
        slots = []
        slots.append(SlotSet(key="monto_promesa", value=promesa_pago['monto_promesa']))
        slots.append(SlotSet(key="nombre_deudor", value=promesa_pago['nombre_deudor']))
        slots.append(SlotSet(key="institucion_deudor", value=promesa_pago['institucion_deudor']))
        slots.append(SlotSet(key="fecha_promesa", value=promesa_pago['fecha_promesa']))
        slots.append(SlotSet(key="fecha_promesa_confirmada", value=None))
        slots.append(SlotSet(key="lugar_pago", value=None))
        slots.append(SlotSet(key="num_operacion", value=promesa_pago['num_operacion']))
        slots.append(SlotSet(key="ppr_codigo", value=promesa_pago['ppr_codigo']))
        slots.append(SlotSet(key="resultado", value="sinconfirmar"))
        return slots

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        # any slots that should be carried over should come after the
        # `session_started` event
        events.extend(self.fetch_slots(tracker))

        # an `action_listen` should be added at the end as a user message follows
        events.append(ActionExecuted("action_listen"))

        return events

class GrabarResultadoAction(Action):

    def name(self) -> Text:

        return "action_grabar_resultado"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Esta accion tiene que grabar en la BD que la PP no la confirmo con el usuario
        Monto_Promesa = tracker.get_slot(key="monto_promesa")
        Nombre_Deudor = tracker.get_slot(key="nombre_deudor")
        Institucion_Deudor = tracker.get_slot(key="institucion_deudor")
        Fecha_Promesa = tracker.get_slot(key="fecha_promesa")
        Fecha_Promesa_Confirmada = tracker.get_slot(key="fecha_promesa_confirmada")
        Lugar_Pago = tracker.get_slot(key="lugar_pago")
        Num_Operacion = tracker.get_slot(key="num_operacion")
        PPR_Codigo = tracker.get_slot(key="ppr_codigo")
        Resultado = tracker.get_slot(key="resultado")
        if Lugar_Pago is not None and Fecha_Promesa_Confirmada is not None:
            Resultado = "confirmada"
        elif tracker.get_slot(key='nuevo_monto_promesa') is not None:
            Resultado = "deudorquierenegociar"
        # elif tracker.last_executed_action_has() == 'utter_informar_promesa_no':
        #    Resultado = "notienetiempo"

        payload = {
            'monto_promesa' : Monto_Promesa,
            'nombre_deudor' : Nombre_Deudor,
            'institucion_deudor': Institucion_Deudor,
            'fecha_promesa' : Fecha_Promesa,
            'fecha_promesa_confirmada' : Fecha_Promesa_Confirmada,
            'lugar_pago' : Lugar_Pago,
            'num_operacion' : Num_Operacion,
            'ppr_codigo' : PPR_Codigo,
            'resultado' : Resultado
        }
        header = {"content-type": "application/json"}
        resultado = requests.post('http://10.123.0.25/webApi/api/resultadopromesa', data=json.dumps(payload), headers=header, verify=False)
        dispatcher.utter_message(text="\n\n Muchas Gracias, hasta pronto!!!")
        return []

