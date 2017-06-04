# commands to deploy freelancefinder application


# Generic Commands #
get_password:
	cat /vagrant/vault-password.file > ~/vault-password.file; cat /vagrant/slack_api_token.file >> ~/freelancefinder/freelancefinder/.env

requirements:
	ansible-galaxy install -r requirements.yml

vault:
	ansible-vault edit --vault-password-file=~/vault-password.file group_vars/all/secrets.yml


# Vagrant specific commands #
bootstrap: get_password requirements
	ansible-playbook -i vagrant bootstrap.yml -e "ansible_ssh_user=ubuntu" -e "ansible_ssh_pass=vagrant" --vault-password-file=~/vault-password.file

vault-vagrant:
	ansible-vault edit --vault-password-file=~/vault-password.file vagrant/group_vars/all/secrets.yml

dbservers:
	ansible-playbook -i vagrant dbservers.yml --vault-password-file=~/vault-password.file

webservers:
	ansible-playbook -i vagrant webservers.yml --vault-password-file=~/vault-password.file

site: requirements
	ansible-playbook -i vagrant site.yml --vault-password-file=~/vault-password.file

deploy:
	ansible-playbook -i vagrant deploy.yml --vault-password-file=~/vault-password.file


# Production/Linode specific commands #
bootstrap-prod: get_password requirements
	ansible-playbook -i production bootstrap.yml -e "ansible_ssh_user=root" --ask-pass --vault-password-file=~/vault-password.file

vault-prod:
	ansible-vault edit --vault-password-file=~/vault-password.file production/group_vars/all/secrets.yml

dbservers-prod:
	ansible-playbook -i production dbservers.yml --vault-password-file=~/vault-password.file

webservers-prod:
	ansible-playbook -i production webservers.yml --vault-password-file=~/vault-password.file

site-prod: requirements
	ansible-playbook -i production site.yml --vault-password-file=~/vault-password.file

deploy-prod:
	ansible-playbook -i production deploy.yml --vault-password-file=~/vault-password.file
