Este arquivo Markdown (README.md) fornece uma documentação completa do código Django para gestão de militares, incluindo detalhes sobre as funcionalidades, modelos, views e tecnologias utilizadas.
Visão Geral

Este projeto Django implementa um sistema para gerenciar informações de militares, incluindo dados pessoais, detalhes da situação, promoções, imagens e histórico de movimentações. O sistema utiliza o sistema de autenticação do Django, mensagens flash para feedback ao usuário e interage com diversos modelos.
Funcionalidades

    Cadastro de Militar (cadastrar_militar):
        Permite o cadastro de novos militares, incluindo dados pessoais, detalhes da situação, promoção e imagem.
        Valida a existência de CPF já cadastrado.
        Utiliza mensagens flash para informar o resultado da operação.

    Listagem de Militares (listar_militar):
        Lista os militares cadastrados, ordenados pelo último posto/graduação.
        Utiliza uma subconsulta para otimizar a busca do último posto/graduação.

    Visualização de Militar (ver_militar):
        Exibe os detalhes de um militar específico, incluindo dados pessoais, detalhes da situação, promoção e informações adicionais (RPT).

    Exclusão de Militar (excluir_militar):
        Permite a exclusão de um militar cadastrado.

    Edição de Posto/Graduação (editar_posto_graduacao):
        Permite a edição das informações de posto/graduação de um militar, mantendo um histórico das alterações.

    Edição de Situação Atual (editar_situacao_atual):
        Permite a edição da situação atual de um militar via requisição AJAX, atualizando apenas os campos necessários.

    Cadastro de Nova Situação (cadastrar_nova_situacao):
        Permite o cadastro de uma nova situação funcional para um militar, mantendo um histórico das alterações.

    Edição de Dados Pessoais e Contatos (editar_dados_pessoais_contatos):
        Permite a edição dos dados pessoais e informações de contato de um militar.

    Edição de Imagem (editar_imagem):
        Permite a atualização da foto de um militar.

    Histórico de Movimentações (historico_movimentacoes):
        Exibe o histórico de promoções e detalhes de situação de um militar.

    Edição de Situação Funcional (editar_situacao_funcional):
        Permite a edição da situação funcional de um militar, incluindo a criação de um histórico.

    Verificação de RPT (check_rpt):
        Verifica se um militar possui cadastro RPT, retornando uma resposta JSON.

Modelos

    Cadastro: Armazena os dados pessoais do militar (RE, Dig, Nome, Nome de Guerra, Gênero, Data de Nascimento, Matrícula, Admissão, Previsão de Inatividade, CPF, RG, Tempo para Averbar INSS, Tempo para Averbar Militar, Email, Telefone).
    DetalhesSituacao: Armazena os detalhes da situação funcional do militar (Situação, SGB, Posto/Seção, Está Adido, Função, Op Adm, Apresentação na Unidade, Saída da Unidade, Categoria de Efetivo).
    Promocao: Armazena as informações de promoção do militar (Posto/Graduação, Quadro, Grupo, Última Promoção).
    Imagem: Armazena a foto do militar.
    HistoricoDetalhesSituacao: Armazena o histórico das alterações na situação funcional.
    HistoricoPromocao: Armazena o histórico das promoções.
    Cadastro_adicional: Armazena informações adicionais do militar (Número Adicional, Data do Último Adicional, Número LP, Data do Último LP).
    Cadastro_rpt: Armazena informações do RPT do militar.

Views (Detalhes)

Cada view é protegida com @login_required, exigindo autenticação do usuário.

    cadastrar_militar(request):
        GET: Exibe o formulário de cadastro.
        POST: Processa o formulário, valida o CPF, cria os objetos nos modelos e redireciona.

    listar_militar(request):
        GET: Lista os militares com paginação e ordenação.

    ver_militar(request, id):
        GET: Exibe os detalhes de um militar específico.

    excluir_militar(request, id):
        GET: Exclui um militar e redireciona para a lista.

    editar_posto_graduacao(request, id):
        GET: Exibe o formulário de edição de posto/graduação.
        POST: Atualiza os dados e o histórico de promoções.

    editar_situacao_atual(request, id):
        POST: Atualiza a situação atual via AJAX.

    cadastrar_nova_situacao(request, id):
        POST: Cadastra uma nova situação e atualiza o histórico.

    editar_dados_pessoais_contatos(request, id):
        GET: Exibe o formulário de edição de dados pessoais e contatos.
        POST: Atualiza os dados.

    editar_imagem(request, id):
        POST: Atualiza a foto do militar.

    historico_movimentacoes(request, id):
        GET: Exibe o histórico de promoções e situações.

    editar_situacao_funcional(request, id):
        POST: Edita a situação funcional e cria um histórico.

    check_rpt(request, id):
        GET: Verifica se o militar possui cadastro RPT e retorna um JSON.

Tecnologias Utilizadas

    Django: Framework web.
    Python: Linguagem de programação.
    Banco de dados: PostgreSQL (presumivelmente).
    HTML/CSS/JavaScript: Frontend.
    AJAX: Requisições dinâmicas.

Como Usar

    Clone o repositório.
    Instale as dependências (pip install -r requirements.txt).
    Configure o banco de dados.
    Execute as migrações (python manage.py migrate).
    Inicie o servidor de desenvolvimento (python manage.py runserver).

Próximos Passos

    Implementar testes unitários.
    Melhorar a interface do usuário.
    Adicionar validações de formulário.
    Implementar paginação.
    Considerar o uso de cache.