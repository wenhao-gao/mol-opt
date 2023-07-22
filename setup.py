import os
import setuptools

this_directory = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'requirements.txt'),
          encoding='utf-8') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name = 'mol-opt',
    version = '0.0.1',
    author = 'Wenhao Gao, Tianfan Fu, Jimeng Sun, Connor Coley',
    author_email = 'gaowh19@gmail.com',
    description = 'Mol-Opt: a toolbox for molecular design',
    url = 'https://github.com/wenhao-gao/mol-opt',
    keywords=['molecular optimization', 'drug discovery', 'drug design', 'artificial intelligence', 'deep learning', 'machine learning'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['test']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'molopt': ['graph_mcts/p1.p', 'graph_mcts/rs_make_ring.p', 'graph_mcts/p_ring.p', 
                            'graph_mcts/rs_ring.p', 'graph_mcts/r_s1.p', 'graph_mcts/size_stats.p',
                            'mimosa/data/substructure.txt', 'mimosa/data/vocabulary.txt', 
                            'mimosa/pretrained_model/GNN.ckpt', 
                            'reinvent/data/Voc', 'reinvent/data/Prior.ckpt', 
                            'reinvent_selfies/data/Voc', 'reinvent_selfies/data/Prior.ckpt', 
                            'smiles_vae/checkpoint/smiles_vae_model_080.pt', 
                            'smiles_vae/checkpoint/smiles_vae_config.pt', 
                            'smiles_vae/checkpoint/smiles_vae_vocab.txt', 
                            'jt_vae/data/zinc/vocab.txt', 
                            'jt_vae/fast_molvae/vae_model/model.iter-25000', ]},
)


