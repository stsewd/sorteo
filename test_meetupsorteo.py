import sys
from unittest import mock

import pytest

import meetupsorteo


def test_procesar_argumentos_evento():
    sys.argv = [sys.executable] + ['evento']
    args = meetupsorteo.get_argparser().parse_args()
    assert args.evento == 'evento'


def test_procesar_argumentos_evento_es_requerido():
    sys.argv = [sys.executable]
    with pytest.raises(SystemExit):
        meetupsorteo.get_argparser().parse_args()


@pytest.mark.parametrize(
    "opcion,esperado",
    [
        ([], 1),
        (['-n', '5'], 5),
        (['--numero', '5'], 5),
    ])
def test_procesar_argumentos_numero(opcion, esperado):
    sys.argv = [sys.executable] + opcion + ['evento']
    args = meetupsorteo.get_argparser().parse_args()
    assert args.numero == esperado


@pytest.mark.parametrize(
    "opcion,esperado",
    [
        ([], False),
        (['--no-abrir-perfil'], True),
    ])
def test_procesar_argumentos_abrir_perfil(opcion, esperado):
    sys.argv = [sys.executable] + opcion + ['evento']
    args = meetupsorteo.get_argparser().parse_args()
    assert args.no_abrir_perfil == esperado


@pytest.mark.parametrize(
    "evento_test,pagina_esperada,evento_esperado",
    [
        # Default
        ('1234', meetupsorteo.DFAULT_PAGINA, '1234'),
        # Con lenguaje
        ('www.meetup.com/es/python/events/1234', 'python', '1234'),
        ('http://www.meetup.com/es/python/events/1234', 'python', '1234'),
        ('https://www.meetup.com/es/python/events/1234/', 'python', '1234'),
        # Sin lenguaje
        ('www.meetup.com/python/events/1234', 'python', '1234'),
        ('http://www.meetup.com/python/events/1234', 'python', '1234'),
        ('https://www.meetup.com/python/events/1234/', 'python', '1234'),
        # Nombre con varios caracteres
        ('www.meetup.com/py-ecuador/events/1234', 'py-ecuador', '1234'),
        ('www.meetup.com/python-1234/events/1234', 'python-1234', '1234'),
    ])
def test_procesar_evento(evento_test, pagina_esperada, evento_esperado):
    pagina, evento = meetupsorteo.procesar_evento(evento_test)
    assert pagina == pagina_esperada
    assert evento == evento_esperado


def _get_asistentes():
    return [
        {
            "member": {
                "id": 1,
                "name": "Uno",
            },
            "rsvp": {
                "response": "yes",
            },
        },
        {
            "member": {
                "id": 2,
                "name": "Dos",
            },
            "rsvp": {
                "response": "yes",
            },
        },
        {
            "member": {
                "id": 3,
                "name": "Tres",
            },
            "rsvp": {
                "response": "no",
            },
        },
    ]


@mock.patch('meetupsorteo.get_asistentes')
def test_selecionar_ganadores_solo_presentes(get_asistentes):
    asistentes = _get_asistentes()
    get_asistentes.return_value = asistentes
    ganadores = list(meetupsorteo.seleccionar_ganadores(
        'cualquier', 'cosa', len(asistentes)
    ))
    # Id 3 no debe estar en esta lista
    assert len(ganadores) == 2
    assert {ganador["member"]["id"] for ganador in ganadores} == {1, 2}


@mock.patch('meetupsorteo.get_asistentes')
@pytest.mark.parametrize('numero', [1, 2])
def test_selecionar_ganadores_n(get_asistentes, numero):
    asistentes = _get_asistentes()
    get_asistentes.return_value = asistentes
    ganadores = list(meetupsorteo.seleccionar_ganadores(
        'cualquier', 'cosa', numero
    ))
    assert len(ganadores) == numero


@mock.patch('webbrowser.open')
def test_mostrar_ganador_abrir_perfil(webbrowser_open):
    ganador = _get_asistentes()[0]
    meetupsorteo.mostrar_ganador(ganador, abrir_perfil=True)
    webbrowser_open.assert_called()


@mock.patch('webbrowser.open')
def test_mostrar_ganador_no_abrir_perfil(webbrowser_open):
    ganador = _get_asistentes()[0]
    meetupsorteo.mostrar_ganador(ganador, abrir_perfil=False)
    webbrowser_open.assert_not_called()


@mock.patch('meetupsorteo.print')
def test_mostrar_ganador_mensaje_correcto(printmock):
    ganador = {
        "member": {
            "id": 1,
            "name": "Uno",
        },
        "rsvp": {
            "response": "yes",
        },
    }
    meetupsorteo.mostrar_ganador(ganador, abrir_perfil=False)
    args, kwargs = printmock.call_args
    assert '¡Felicitacines Uno!' in args[0]


@mock.patch('meetupsorteo.procesar_evento')
@mock.patch('meetupsorteo.get_argparser')
def test_main_captura_excepcion(get_argparser, procesar_evento):
    procesar_evento.side_effect = Exception
    with pytest.raises(SystemExit):
        meetupsorteo.main()


@mock.patch('meetupsorteo.mostrar_ganador')
@mock.patch('meetupsorteo.seleccionar_ganadores')
@mock.patch('meetupsorteo.procesar_evento')
@mock.patch('meetupsorteo.get_argparser')
def test_main_flujo_completo(
        get_argparser, procesar_evento,
        seleccionar_ganadores, mostrar_ganador):
    asistentes = _get_asistentes()
    procesar_evento.return_value = (mock.Mock(), mock.Mock())
    seleccionar_ganadores.return_value = asistentes

    meetupsorteo.main()

    get_argparser.assert_called_once()
    procesar_evento.assert_called_once()
    seleccionar_ganadores.assert_called_once()
    assert len(mostrar_ganador.mock_calls) == len(asistentes)
