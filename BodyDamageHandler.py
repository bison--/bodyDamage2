import dearpygui.dearpygui as dpg
from typing import Union


class BodyDamageHandler:

    def __init__(self):
        self.connectedBodyParts = {
            'LBody': ('RLeg', 'LLeg'),
            'RLeg': ('RFeet',),
            'LLeg': ('LFeet',),
            'RArm': ('RHand',),
            'LArm': ('LHand',)
        }

        self.pgbHP = None  # type: Union[int : str]
        self.txtReport = None  # type: Union[int : str]

    def calculate(self, sender, app_dat):
        lostSubBodyPart = False
        totalHp = 0
        restHp = 0
        dead = False
        damageResult = []
        additionalMessages = []

        for itm in dpg.get_all_items():
            item_alias = dpg.get_item_alias(itm)
            if item_alias.startswith('sld'):
                tmpValue = dpg.get_value(itm)
                # TODO: get item value
                tmpMax = 100
                totalHp += tmpMax
                restHp += tmpValue

                if tmpValue < tmpMax and tmpValue > 0:
                    damageResult.append(dpg.get_item_label(itm) + ": {0:d} %".format(tmpValue))
                elif tmpValue == 0:
                    damageResult.append("You lost: " + dpg.get_item_label(itm))
                    itmShort = item_alias.replace('sld', '')
                    if itmShort in self.connectedBodyParts:
                        for subPart in self.connectedBodyParts[itmShort]:
                            if dpg.get_value('sld' + subPart) > 0:
                                dpg.set_value('sld' + subPart, 0)
                                lostSubBodyPart = True

                if item_alias == 'sldHead' and tmpValue == 0:
                    additionalMessages.append("DONT LOSE YOUR HEAD!")
                    dead = True
                elif item_alias == 'sldUBody' and tmpValue == 0:
                    additionalMessages.append("seems like your heard stopped beating...")
                    dead = True

            elif item_alias.startswith('chk'):
                totalHp += 50
                if not dpg.get_value(itm):
                    restHp += 50
                else:
                    additionalMessages.append("NO MORE ADVENTURES 4 YOU")

        if lostSubBodyPart:
            self.calculate(sender, app_dat)
        else:
            if dead or restHp <= 0:
                additionalMessages.append("DEAD")
                dpg.set_value(self.pgbHP, 0)
                #dpg.bind_theme('Cherry')
                #dpg.bind_item_theme('mainWindow', 'Cherry')
            else:
                #dpg.bind_item_theme('mainWindow', 'Dark')
                #dpg.bind_theme('Dark')
                self.set_progress_bar_value(restHp, totalHp)

            finalText = "{0}/{1} hp\n".format(restHp, totalHp)
            if damageResult:
                finalText += "\n".join(damageResult)

            if finalText != "" and additionalMessages:
                finalText += "\n"

            if additionalMessages:
                finalText += "\n".join(additionalMessages)

            dpg.set_value(self.txtReport, finalText)

    def heal(self, sender, app_dat):
        print('heal', sender, app_dat)

        for itm in dpg.get_all_items():
            item_alias = dpg.get_item_alias(itm)
            if item_alias.startswith('sld'):
                dpg.set_value(itm, 100)
            elif item_alias.startswith('chk'):
                dpg.set_value(itm, False)

        self.calculate(sender, app_dat)

    def set_progress_bar_value(self, value, max):
        percentage = value / max
        dpg.set_value(self.pgbHP, percentage)
