describe('I can read only overview page', () => {

    beforeEach(() => {
        cy.login("jeannot");
    })

    it('goes to recommandations and read only content', () => {

        cy.visit('/projects')

        cy.contains('Friche numéro 1').click({force:true});

        cy.contains("Recommandations").click({ force: true })

        cy.url().should('include', '/actions')

        cy.contains("Ajouter une recommandation").should('not.exist')
    })
})
