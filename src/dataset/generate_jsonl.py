import json
import os
from typing import List, Dict, Any


REQUIRED_KEYS = ("id", "pergunta", "resposta", "capitulo", "pagina", "trecho")


def validate_dataset(data: List[Dict[str, Any]]) -> None:
    if not isinstance(data, list):
        raise TypeError(f"data deve ser uma lista, veio: {type(data).__name__}")

    for idx, entry in enumerate(data, start=1):
        if not isinstance(entry, dict):
            raise TypeError(f"Registro #{idx} deve ser dict, veio: {type(entry).__name__}")

        missing = [k for k in REQUIRED_KEYS if k not in entry]
        if missing:
            raise ValueError(f"Registro #{idx} está sem chaves obrigatórias: {missing}")

        try:
            json.dumps(entry, ensure_ascii=False)
        except TypeError as e:
            raise TypeError(f"Registro #{idx} não é serializável em JSON: {e}") from e



def generate_jk_jsonl(data: List[Dict[str, Any]], output_path: str) -> None:
    """
    Converte uma lista de dicionários no formato JSONL (JSON Lines).
    
    Args:
        data (List[Dict[str, Any]]): Lista contendo os 40 pares de P&R de JK.
        output_path (str): Caminho completo onde o arquivo .jsonl será salvo.
    
    Returns:
        None
    """

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        validate_dataset(data)
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in data:
                json_record = json.dumps(entry, ensure_ascii=False)
                f.write(json_record + "\n")

        print(f"✅ Sucesso! Dataset gerado em: {output_path}")
        print(f"📊 Total de registros: {len(data)}")
    except Exception as e:
        print(f"❌ Erro ao gerar o arquivo: {e}")

if __name__ == "__main__":
    # O seu dataset bruto (truncado aqui para brevidade, mas você deve usar a lista completa)
    jk_data = [
  {
    "id": "1",
    "pergunta": "Onde nasceu Juscelino Kubitschek?",
    "resposta": "Em Diamantina, Minas Gerais.",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "37",
    "trecho": "Começo da manhã de 12 de setembro de 1902 na bela Diamantina... Chega ao mundo Juscelino Kubitschek de Oliveira..."
  },
  {
    "id": "2",
    "pergunta": "Qual era o nome do pai de Juscelino?",
    "resposta": "João César de Oliveira.",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "37",
    "trecho": "Pai: o jovem e irrequieto João César de Oliveira, que já fora garimpeiro, caixeiro-viajante..."
  },
  {
    "id": "3",
    "pergunta": "Qual era o apelido de infância de Juscelino?",
    "resposta": "Nonô.",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "37",
    "trecho": "...menino sadio que ganhará o apelido de Nonô."
  },
  {
    "id": "4",
    "pergunta": "De onde veio o bisavô materno de JK, Jan Nepomuscky Kubitschek?",
    "resposta": "De Trebon, Boêmia (Tchecoslováquia).",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "40",
    "trecho": "Viera de Trebon, Boêmia, Tchecoslováquia, então parte do império austro-húngaro."
  },
  {
    "id": "5",
    "pergunta": "De que doença morreu o pai de Juscelino em 1905?",
    "resposta": "Tuberculose.",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "41",
    "trecho": "João César partiu em 10 de janeiro de 1905, vítima de tuberculose, que se seguiu a forte pneumonia..."
  },
  {
    "id": "6",
    "pergunta": "Qual era a profissão da mãe de Juscelino, Júlia Kubitschek?",
    "resposta": "Professora primária.",
    "capitulo": "Capítulo 1 - O menino de Diamantina",
    "pagina": "37",
    "trecho": "Mãe: Júlia Kubitschek, normalista, professora primária."
  },
  {
    "id": "7",
    "pergunta": "Em qual órgão JK começou a trabalhar como concursado em 1921?",
    "resposta": "Nos Correios (Repartição Geral dos Telégrafos).",
    "capitulo": "Capítulo 2 - Telegrafista, acadêmico, médico",
    "pagina": "51",
    "trecho": "Será aproveitado como telegrafista-auxiliar... Seu horário nos Correios era de meia-noite às seis."
  },
  {
    "id": "8",
    "pergunta": "Quem foi o grande amigo de JK e marido de sua irmã Naná?",
    "resposta": "Júlio Soares.",
    "capitulo": "Capítulo 2 - Telegrafista, acadêmico, médico",
    "pagina": "52",
    "trecho": "Doutor Júlio será o amigo mais próximo de toda a vida de Juscelino... Além de médico, era um caráter admirável."
  },
  {
    "id": "9",
    "pergunta": "Em que data exata Juscelino se formou em medicina?",
    "resposta": "17 de dezembro de 1927.",
    "capitulo": "Capítulo 3 - Doutor Juscelino e Sarah",
    "pagina": "55",
    "trecho": "Diplomado em 17 de dezembro de 1927, deixa os Correios."
  },
  {
    "id": "10",
    "pergunta": "Com quem Juscelino se casou no ano de 1931?",
    "resposta": "Sarah Luísa Lemos (Sarah Kubitschek).",
    "capitulo": "Capítulo 3 - Doutor Juscelino e Sarah",
    "pagina": "56",
    "trecho": "Casa-se com Sarah em 30 de dezembro de 1931, no Rio de Janeiro, Ipanema, Igreja da Paz."
  },
  {
    "id": "11",
    "pergunta": "Qual foi a patente e a função militar de JK na Revolução de 1932?",
    "resposta": "Capitão-médico da Força Pública de Minas Gerais.",
    "capitulo": "Capítulo 4 - Batismo de fogo, batismo político",
    "pagina": "57",
    "trecho": "...nomeado, por decreto de 17 de março de 1932, capitão-médico da Força Pública de Minas Gerais."
  },
  {
    "id": "12",
    "pergunta": "Em qual cidade mineira JK montou um improvisado hospital de sangue em 1932?",
    "resposta": "Passa Quatro.",
    "capitulo": "Capítulo 4 - Batismo de fogo, batismo político",
    "pagina": "59",
    "trecho": "Juscelino foi mandado de volta a Passa Quatro no primeiro dia. Missão urgente: montar hospital de sangue."
  },
  {
    "id": "13",
    "pergunta": "Qual político nomeou JK para a chefia da Casa Civil de Minas Gerais em 1933?",
    "resposta": "Benedito Valadares.",
    "capitulo": "Capítulo 5 - A relutante inserção na vida pública",
    "pagina": "65",
    "trecho": "A nomeação chegara-lhe de imprevisto... E soltou a bomba, que me deixou perplexo: 'Você, por exemplo, será o chefe de minha Casa Civil'."
  },
  {
    "id": "14",
    "pergunta": "Para qual cargo legislativo Juscelino foi eleito nas eleições de 1934?",
    "resposta": "Deputado federal.",
    "capitulo": "Capítulo 6 - Deputado federal Juscelino Kubitschek",
    "pagina": "71",
    "trecho": "Na eleição, fui o deputado mais votado, com 32 anos... Toma posse no Palácio Tiradentes, Rio de Janeiro, em 3 de maio de 1935."
  },
  {
    "id": "15",
    "pergunta": "Qual evento político fez JK perder seu mandato parlamentar em 10 de novembro de 1937?",
    "resposta": "O golpe do Estado Novo.",
    "capitulo": "Capítulo 6 - Deputado federal Juscelino Kubitschek",
    "pagina": "75",
    "trecho": "Na madrugada de 10 de novembro de 1937, Vargas golpeia. Fulmina as eleições, dissolve o Congresso, anula todos os mandatos parlamentares... Nasce o Estado Novo."
  },
  {
    "id": "16",
    "pergunta": "Qual cargo JK assumiu em 16 de abril de 1940, voltando à vida pública?",
    "resposta": "Prefeito de Belo Horizonte.",
    "capitulo": "Capítulo 7 - Volta à medicina",
    "pagina": "78",
    "trecho": "...publique decreto, já assinado, de nomeação de Juscelino para o cargo de prefeito de Belo Horizonte..."
  },
  {
    "id": "17",
    "pergunta": "Qual apelido Juscelino ganhou do povo ao revolucionar obras na prefeitura?",
    "resposta": "Prefeito Furacão.",
    "capitulo": "Introdução - Há muita grandeza em JK",
    "pagina": "30",
    "trecho": "O povo o apelidou de Prefeito Furacão, porque balançou a cidade, mexeu em tudo, espalhou obras e inovações por toda banda."
  },
  {
    "id": "18",
    "pergunta": "Qual era o nome do motorista de JK que o acompanhou a vida toda?",
    "resposta": "Geraldo Ribeiro.",
    "capitulo": "Capítulo 8 - Prefeito de Belo Horizonte",
    "pagina": "82",
    "trecho": "...apresenta o motorista que serve ao prefeito, Geraldo Ribeiro... Ganhará de Juscelino o apelido de Platão..."
  },
  {
    "id": "19",
    "pergunta": "Qual arquiteto JK convocou para projetar o complexo da Pampulha?",
    "resposta": "Oscar Niemeyer.",
    "capitulo": "Capítulo 8 - Prefeito de Belo Horizonte",
    "pagina": "84",
    "trecho": "Convoca o jovem Oscar Niemeyer para arquitetar sua primeira grande obra pública: o novo bairro da Pampulha."
  },
  {
    "id": "20",
    "pergunta": "Qual partido JK ajudou a fundar e a estruturar em Minas Gerais em 1945?",
    "resposta": "PSD (Partido Social Democrático).",
    "capitulo": "Capítulo 9 - Deputado federal constituinte",
    "pagina": "87",
    "trecho": "Juscelino se engaja na fundação do Partido Social Democrático de Minas Gerais..."
  },
  {
    "id": "21",
    "pergunta": "Na Constituinte de 1946, onde JK propôs oficialmente que fosse localizada a nova capital?",
    "resposta": "No Triângulo Mineiro.",
    "capitulo": "Capítulo 9 - Deputado federal constituinte",
    "pagina": "94",
    "trecho": "...formaliza proposta de localizá-la na 'região central compreendida entre os rios Paranaíba e Grande'. Isto é, no Triângulo Mineiro..."
  },
  {
    "id": "22",
    "pergunta": "Para qual cargo executivo JK foi eleito nas eleições de 3 de outubro de 1950?",
    "resposta": "Governador de Minas Gerais.",
    "capitulo": "Capítulo 10 - Governador de Minas Gerais",
    "pagina": "101",
    "trecho": "Candidatou-se ao governo de Minas pela oposição e ganhou do Gabriel Passos."
  },
  {
    "id": "23",
    "pergunta": "Qual foi a síntese adotada como base de ação de seu governo em Minas?",
    "resposta": "Energia e Transportes.",
    "capitulo": "Capítulo 10 - Governador de Minas Gerais",
    "pagina": "106",
    "trecho": "A base de ação seria o binômio Energia e Transportes."
  },
  {
    "id": "24",
    "pergunta": "Qual presidente da República deu apoio vital à gestão de JK como governador?",
    "resposta": "Getúlio Vargas.",
    "capitulo": "Capítulo 10 - Governador de Minas Gerais",
    "pagina": "102",
    "trecho": "O apoio firme do presidente terá peso decisivo na realização do programa administrativo e sonhos políticos do diamantinense."
  },
  {
    "id": "25",
    "pergunta": "Qual político do PTB foi o candidato a vice-presidente na chapa de JK em 1955?",
    "resposta": "João Goulart (Jango).",
    "capitulo": "Capítulo 11 - Candidatura e campanha presidencial",
    "pagina": "126",
    "trecho": "A aliança com o PTB, João Goulart de vice, é formalizada no começo de dezembro de 1954."
  },
  {
    "id": "26",
    "pergunta": "Em qual cidade de Goiás JK fez o comício prometendo a construção de Brasília?",
    "resposta": "Jataí.",
    "capitulo": "Capítulo 11 - Candidatura e campanha presidencial",
    "pagina": "129",
    "trecho": "Jataí, sertão goiano, 4 de abril de 1955... Cumprirei na íntegra a Constituição. Durante o meu quinquênio, farei a mudança da sede do governo e construirei a nova capital."
  },
  {
    "id": "27",
    "pergunta": "Qual general liderou o contragolpe de 11 de novembro de 1955, garantindo a posse de JK?",
    "resposta": "General Henrique Teixeira Lott.",
    "capitulo": "Capítulo 11 - Candidatura e campanha presidencial",
    "pagina": "136",
    "trecho": "É o golpe preventivo de Lott, o 11 de Novembro. Trata-se, na verdade, de um contragolpe, porque garantiu a posse do presidente eleito..."
  },
  {
    "id": "28",
    "pergunta": "Qual era o nome do arrojado plano de desenvolvimento lançado por JK no primeiro dia de presidência?",
    "resposta": "Programa de Metas.",
    "capitulo": "Capítulo 12 - A Era JK",
    "pagina": "144",
    "trecho": "Lança o arrojado Programa de Metas... Suas 31 metas estão assim desdobradas..."
  },
  {
    "id": "29",
    "pergunta": "O que representava a \"meta-síntese\" do Programa de Metas?",
    "resposta": "A construção de Brasília.",
    "capitulo": "JK por Celso Lafer",
    "pagina": "446",
    "trecho": "...e também a meta-síntese, que foi a construção de Brasília."
  },
  {
    "id": "30",
    "pergunta": "Em que data exata a nova capital Brasília foi inaugurada?",
    "resposta": "21 de abril de 1960.",
    "capitulo": "Inauguração de Brasília",
    "pagina": "360",
    "trecho": "Neste dia 21 de abril consagrado ao alferes Joaquim José da Silva Xavier, o Tiradentes, ao centésimo trigésimo oitavo ano da Independência e septuagésimo primeiro da República, declaro, sob a proteção de Deus, inaugurada a cidade de Brasília, capital dos Estados Unidos do Brasil."
  },
  {
    "id": "31",
    "pergunta": "Por qual estado JK se elegeu senador com expressiva votação no ano de 1961?",
    "resposta": "Goiás.",
    "capitulo": "Capítulo 13 - Senador da República",
    "pagina": "169",
    "trecho": "Nas eleições de 4 de junho de 1961, JK venceu o destacado líder político\nWagner Estelita Campos, do PDC, apoiado pelo presidente Jânio Quadros. Obteve 84,5% dos votos."
  },
  {
    "id": "32",
    "pergunta": "Qual era o slogan famoso de sua antecipada campanha presidencial para 1965?",
    "resposta": "JK-65: cinco anos de agricultura para cinquenta de fartura.",
    "capitulo": "Capítulo 13 - Senador da República",
    "pagina": "165",
    "trecho": "Tinha até slogan, de todos conhecido: 'JK-65: cinco anos de agricultura para cinquenta de fartura.'"
  },
  {
    "id": "33",
    "pergunta": "Em que data o regime militar cassou os direitos políticos de Juscelino?",
    "resposta": "8 de junho de 1964.",
    "capitulo": "Decreto de cassação do mandato e dos direitos políticos do senador Juscelino Kubitschek de Oliveira",
    "pagina": "430",
    "trecho": "Cassar o mandato legislativo e suspender os direitos políticos por dez anos do senador Juscelino Kubitschek de Oliveira. Brasília, 8 de junho de 1964"
  },
  {
    "id": "34",
    "pergunta": "Qual general, então presidente da República, assinou o decreto de sua cassação?",
    "resposta": "Castello Branco",
    "capitulo": "Decreto de cassação do mandato e dos direitos políticos do senador Juscelino Kubitschek de Oliveira",
    "pagina": "430",
    "trecho": "Cassar o mandato legislativo... H. Castello Branco"
  },
  {
    "id": "35",
    "pergunta": "Qual país europeu serviu como sua primeira morada durante o período de exílio?",
    "resposta": "França (Paris).",
    "capitulo": "Capítulo 15 - Exílio e sofrimento",
    "pagina": "200",
    "trecho": "Em Paris, por exemplo, mora num apartamento pequeno, na Boulevard Lannes..."
  },
  {
    "id": "36",
    "pergunta": "Qual movimento político de oposição JK articulou em Lisboa com Lacerda e Goulart em 1966?",
    "resposta": "Frente Ampla.",
    "capitulo": "Capítulo 15 - Exílio e sofrimento",
    "pagina": "211",
    "trecho": "...lançara... o manifesto da Frente Ampla. Do encontro sai a Declaração de Lisboa, redigida às pressas por Lacerda, com contribuições de JK..."
  },
  {
    "id": "37",
    "pergunta": "Para qual academia de letras estadual JK foi eleito por unanimidade em 1974?",
    "resposta": "Academia Mineira de Letras.",
    "capitulo": "Capítulo 16 - Volta ao Brasil",
    "pagina": "235",
    "trecho": "Fevereiro de 1974, candidata-se à cadeira nº 34 da Academia Mineira de Letras... Foi eleito, por unanimidade, em junho de 1974."
  },
  {
    "id": "38",
    "pergunta": "Qual era o nome da propriedade rural que JK adquiriu no município goiano de Luziânia?",
    "resposta": "Fazendinha JK.",
    "capitulo": "Capítulo 17 - A morte na curva da estrada",
    "pagina": "261",
    "trecho": "Em 1972, compra terras em Luziânia... para formar a Fazendinha JK..."
  },
  {
    "id": "39",
    "pergunta": "Qual foi a data e o local exato do acidente automobilístico fatal de JK?",
    "resposta": "22 de agosto de 1976, na Via Dutra (Km 165, Resende).",
    "capitulo": "Capítulo 17 - A morte na curva da estrada",
    "pagina": "250",
    "trecho": "Às 17h55, na curva do quilômetro 165, município de Resende... JK e Geraldo morrem instantaneamente... 22 de agosto de 1976."
  },
  {
    "id": "40",
    "pergunta": "Onde repousam definitivamente os restos mortais de JK em Brasília (desde 1981)?",
    "resposta": "No Memorial JK.",
    "capitulo": "Capítulo 17 - A morte na curva da estrada",
    "pagina": "243",
    "trecho": "12 de setembro, data em que completaria 79 anos: o general João Baptista de Oliveira Figueiredo, presidente da República, ao lado de dona Sarah Kubitschek, inaugura em Brasília o Memorial JK, monumento e centro de cultura, onde estão seus restos mortais"
  }
]
    
    # Define o caminho de saída baseado na estrutura que vimos anteriormente
    output_file = os.path.join("kb", "processed", "jk_gold_standard.jsonl")
    
    generate_jk_jsonl(jk_data, output_file)