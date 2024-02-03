import os

from pyrogram import Client
from pyrogram.raw.functions.auth import LogOut
from pyrogram.raw.functions.account import UpdateStatus


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.client import Menu_callback, k_work_menu, cancel_upl, k_menu
from data import chats, users
from main import bot

class Acc(StatesGroup):
    session = State()
    chats = State()


API_TOKEN = 'ваш_токен_для_aiogram'
PYROGRAM_SESSION_NAME = 'session_name'
PHONE_NUMBER = 'ваш_номер_телефона'


router = Router()



    




