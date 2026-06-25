"""Tests para los modelos Pydantic de validación."""

from src.utils.models import (
    FacturaExtraida,
    ConceptoFacturacion,
    Totales,
    _to_float,
)


class TestToFloat:
    def test_handles_european_format(self):
        assert _to_float("1.549,19") == 1549.19

    def test_handles_currency_prefix(self):
        assert _to_float("B/. 42,68") == 42.68
        assert _to_float("$ 100.50") == 100.50

    def test_handles_empty(self):
        assert _to_float("") == 0.0
        assert _to_float(None) == 0.0

    def test_handles_numbers(self):
        assert _to_float(42) == 42.0
        assert _to_float(42.5) == 42.5

    def test_handles_invalid(self):
        assert _to_float("abc") == 0.0


class TestConceptoFacturacion:
    def test_normalizes_importe(self):
        c = ConceptoFacturacion(concepto="Cargo Fijo", importe="1.549,19")
        assert c.importe == 1549.19
        assert c.concepto == "Cargo Fijo"


class TestTotales:
    def test_all_fields_normalized(self):
        t = Totales(
            total_mes="100,50",
            gran_total="B/. 200,00",
            saldo_anterior=50,
            saldo_corte="",
        )
        assert t.total_mes == 100.50
        assert t.gran_total == 200.00
        assert t.saldo_anterior == 50.0
        assert t.saldo_corte == 0.0


class TestFacturaExtraida:
    def test_safe_parse_empty(self):
        f = FacturaExtraida.safe_parse({})
        assert f.totales.total_mes == 0.0
        assert f.conceptos_facturacion == []

    def test_safe_parse_partial(self):
        raw = {
            "datos_factura": {"numero_factura": "F-001"},
            "totales": {"total_mes": "1.000,00", "gran_total": "1.500,00"},
            "conceptos_facturacion": [
                {"concepto": "Energía", "importe": "750,00"},
                {"concepto": "Cargo Fijo", "importe": 50.0},
            ],
        }
        f = FacturaExtraida.safe_parse(raw)
        assert f.datos_factura.numero_factura == "F-001"
        assert f.totales.total_mes == 1000.0
        assert f.totales.gran_total == 1500.0
        assert len(f.conceptos_facturacion) == 2
        assert f.conceptos_facturacion[0].importe == 750.0

    def test_safe_parse_handles_garbage(self):
        # Datos completamente inválidos no deben tirar la app
        f = FacturaExtraida.safe_parse({"totales": "not a dict"})
        assert f.totales.total_mes == 0.0
